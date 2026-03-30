"""
The agentic loop as a Temporal workflow.

Your job: wire up the workflow so the agentic loop runs durably.

The activities are already implemented in activities.py.
The run scripts are ready to go.

Work through the TODOs below in order.
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


# TODO 1: Add the @workflow.defn decorator to this class.
class WeatherAgentWorkflow:

    # TODO 2: Add the @workflow.run decorator to this method.
    async def run(self, query: str) -> str:
        messages = [{"role": "user", "content": query}]

        while True:
            # TODO 3: Call the call_llm activity using workflow.execute_activity().
            #
            # Hints:
            #   - Pass args=[messages, TOOLS]
            #   - Set start_to_close_timeout=timedelta(seconds=30)
            #   - Set retry_policy=RetryPolicy(maximum_attempts=1)
            #     (LLM calls should not be retried automatically)
            #
            # Assign the result to `response`.
            response = None  # replace this

            choice = response["choices"][0]["message"]
            messages.append(choice)

            # If the LLM returned a final answer, return it.
            if not choice.get("tool_calls"):
                return choice["content"]

            # TODO 4: For each tool call, execute the matching activity.
            #
            # The structure is already here — replace each `result = None`
            # with a workflow.execute_activity() call for the correct activity.
            #
            # Hints:
            #   - get_weather_alerts takes a single string: tool_args["state"]
            #   - get_coordinates takes a single string: tool_args["location"]
            #   - get_distance_km takes four floats: lat1, lon1, lat2, lon2
            #   - For dict results, wrap in json.dumps() before appending
            for tool_call in choice["tool_calls"]:
                tool_name = tool_call["function"]["name"]
                tool_args = json.loads(tool_call["function"]["arguments"])

                if tool_name == "get_weather_alerts":
                    result = None  # replace this

                elif tool_name == "get_coordinates":
                    result = None  # replace this

                elif tool_name == "get_distance_km":
                    result = None  # replace this

                else:
                    result = f"Unknown tool: {tool_name}"

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": result,
                    }
                )
