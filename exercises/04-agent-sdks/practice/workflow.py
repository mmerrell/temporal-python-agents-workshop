"""
Exercise 04b: Making the SDK agent durable with Temporal.

The agent definition from agent_raw.py stays exactly the same.
Your job: wire it up inside a Temporal workflow using the Temporal + OpenAI Agents integration.

Key insight: instead of @function_tool, activities become tools via
openai_agents.workflow.activity_as_tool(). The SDK still runs the agentic
loop — Temporal handles durability.
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


# TODO 1: Add the @workflow.defn decorator.
class WeatherAgentWorkflow:

    # TODO 2: Add the @workflow.run decorator.
    async def run(self, query: str) -> str:

        # TODO 3: Define the Agent.
        #
        # Use the same name and instructions as agent_raw.py.
        # For tools, wrap each activity with:
        #   openai_agents.workflow.activity_as_tool(
        #       <activity_function>,
        #       start_to_close_timeout=timedelta(seconds=10),
        #   )
        #
        # Activities to wrap: get_weather_alerts, get_coordinates, get_distance_km
        agent = None  # replace this

        # TODO 4: Run the agent and return the final output.
        #
        # Hint: await Runner.run(agent, query)
        # The result has a .final_output attribute.
        pass  # replace this
