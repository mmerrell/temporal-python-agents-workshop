"""
Section 2: Building a Durable Agent from Scratch
solution/workflow.py — reference implementation
"""

import json
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import call_llm, get_weather_alerts, TOOLS


@workflow.defn
class WeatherAgentWorkflow:

    @workflow.run
    async def run(self, query: str) -> str:
        messages = [{"role": "user", "content": query}]

        while True:
            response = await workflow.execute_activity(
                call_llm,
                args=[messages, TOOLS],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=RetryPolicy(maximum_attempts=1),
            )

            choice = response["choices"][0]["message"]
            messages.append(choice)

            if not choice.get("tool_calls"):
                return choice["content"]

            for tool_call in choice["tool_calls"]:
                tool_name = tool_call["function"]["name"]
                tool_args = json.loads(tool_call["function"]["arguments"])

                if tool_name == "get_weather_alerts":
                    result = await workflow.execute_activity(
                        get_weather_alerts,
                        args=[tool_args.get("state", "")],
                        start_to_close_timeout=timedelta(seconds=10),
                    )
                else:
                    result = f"Unknown tool: {tool_name}"

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": result,
                })
