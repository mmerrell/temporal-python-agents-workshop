"""
Section 2: Building a Durable Agent from Scratch
practice/run_starter.py

Submits a WeatherAgentWorkflow to the Temporal server and
prints the result. Run in Terminal 2 while the worker is running.

Usage:
    python run_starter.py "What are the active weather alerts in California?"
"""

import asyncio
import sys
import time

from temporalio.client import Client
from workflow import WeatherAgentWorkflow


async def main(query: str):
    client = await Client.connect("localhost:7233")

    workflow_id = f"weather-agent-{int(time.time())}"
    print(f"\nStarting workflow: {workflow_id}")
    print(f"Query: {query}\n")

    result = await client.execute_workflow(
        WeatherAgentWorkflow.run,
        query,
        id=workflow_id,
        task_queue="weather-agent",
    )

    print(f"Result:\n{result}\n")
    print(f"View in Temporal UI: http://localhost:8080/namespaces/default/workflows/{workflow_id}")


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else \
        "What are the active weather alerts in California?"
    asyncio.run(main(query))
