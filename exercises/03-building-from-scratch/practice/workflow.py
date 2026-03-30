"""
Section 2: Building a Durable Agent from Scratch
practice/workflow.py

The agentic loop lives inside a Temporal workflow.
LLM calls and tool calls are both activities.

Run with:
    python run_worker.py          (Terminal 1)
    python run_starter.py "..."   (Terminal 2)
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
            # Call the LLM as an activity.
            # Non-deterministic I/O must never happen directly in a workflow.
            # RetryPolicy(maximum_attempts=1) because blindly retrying an LLM
            # call gives a different response — handle errors in your own logic.
            response = await workflow.execute_activity(
                call_llm,
                args=[messages, TOOLS],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=RetryPolicy(maximum_attempts=1),
            )

            choice = response["choices"][0]["message"]
            messages.append(choice)

            # No tool calls — the LLM is done.
            if not choice.get("tool_calls"):
                return choice["content"]

            # Execute each tool call as an activity.
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
