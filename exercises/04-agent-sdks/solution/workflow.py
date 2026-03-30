"""
Exercise 04b: Making the SDK agent durable with Temporal.

The agent definition is identical to agent_raw.py.
The only difference: it runs inside a Temporal workflow.

Key pattern: activities become tools via openai_agents.workflow.activity_as_tool().
The SDK still manages the agentic loop. Temporal manages durability.

Open the Temporal UI while this runs — the event history looks exactly
like Exercise 03. Same structure, whether you hand-roll the loop or use the SDK.
"""

from datetime import timedelta

from agents import Agent, Runner
from temporalio import workflow
from temporalio.contrib import openai_agents

with workflow.unsafe.imports_passed_through():
    from activities import (
        get_coordinates,
        get_distance_km,
        get_weather_alerts,
    )


@workflow.defn
class WeatherAgentWorkflow:
    @workflow.run
    async def run(self, query: str) -> str:
        agent = Agent(
            name="Weather Agent",
            instructions=(
                "You are a helpful assistant that answers questions about weather "
                "alerts and distances between locations. Use your tools to look up "
                "real data."
            ),
            tools=[
                # activity_as_tool() wraps each activity as an SDK tool.
                # The SDK calls the tool; Temporal routes it through an activity.
                # Retries, timeouts, and observability come for free.
                openai_agents.workflow.activity_as_tool(
                    get_weather_alerts,
                    start_to_close_timeout=timedelta(seconds=10),
                ),
                openai_agents.workflow.activity_as_tool(
                    get_coordinates,
                    start_to_close_timeout=timedelta(seconds=10),
                ),
                openai_agents.workflow.activity_as_tool(
                    get_distance_km,
                    start_to_close_timeout=timedelta(seconds=10),
                ),
            ],
        )

        result = await Runner.run(agent, query)
        return result.final_output
