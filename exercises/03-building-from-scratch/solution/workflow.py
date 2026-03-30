"""
The agentic loop as a Temporal workflow.

The workflow owns the loop and the state.
LLM calls and tool calls are activities — all I/O stays outside the workflow.
"""

import json
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import (
        call_llm,
        get_coordinates,
        get_distance_km,
        get_weather_alerts,
        TOOLS,
    )


@workflow.defn
class WeatherAgentWorkflow:
    @workflow.run
    async def run(self, query: str) -> str:
        messages = [{"role": "user", "content": query}]

        while True:
            # Call the LLM as an activity.
            # Retries are disabled — LLM responses are non-deterministic,
            # so retrying a failed call would give a different result.
            response = await workflow.execute_activity(
                call_llm,
                args=[messages, TOOLS],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=RetryPolicy(maximum_attempts=1),
            )

            choice = response["choices"][0]["message"]
            messages.append(choice)

            # If the LLM returned a final answer, we're done.
            if not choice.get("tool_calls"):
                return choice["content"]

            # Otherwise execute each tool call as an activity.
            for tool_call in choice["tool_calls"]:
                tool_name = tool_call["function"]["name"]
                tool_args = json.loads(tool_call["function"]["arguments"])

                if tool_name == "get_weather_alerts":
                    result = await workflow.execute_activity(
                        get_weather_alerts,
                        args=[tool_args["state"]],
                        start_to_close_timeout=timedelta(seconds=10),
                    )
                elif tool_name == "get_coordinates":
                    coords = await workflow.execute_activity(
                        get_coordinates,
                        args=[tool_args["location"]],
                        start_to_close_timeout=timedelta(seconds=10),
                    )
                    result = json.dumps(coords)
                elif tool_name == "get_distance_km":
                    dist = await workflow.execute_activity(
                        get_distance_km,
                        args=[
                            tool_args["lat1"],
                            tool_args["lon1"],
                            tool_args["lat2"],
                            tool_args["lon2"],
                        ],
                        start_to_close_timeout=timedelta(seconds=5),
                    )
                    result = json.dumps(dist)
                else:
                    result = f"Unknown tool: {tool_name}"

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": result,
                    }
                )
