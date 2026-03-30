"""
Submit a WeatherAgentWorkflow and print the result.

Usage:
    python run_starter.py "What are the weather alerts for California?"
    python run_starter.py "How far is it from San Francisco to Los Angeles?"
"""

import asyncio
import sys
import time

from temporalio.client import Client

from workflow import WeatherAgentWorkflow


async def main(query: str):
    client = await Client.connect("127.0.0.1:7233")

    workflow_id = f"weather-agent-{int(time.time())}"
    print(f"\nStarting workflow: {workflow_id}")
    print(f"Query: {query}\n")

    result = await client.execute_workflow(
        WeatherAgentWorkflow.run,
        query,
        id=workflow_id,
        task_queue="weather-agent",
    )

    print(f"Result:\n{result}")


if __name__ == "__main__":
    query = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "What are the active weather alerts in California?"
    )
    asyncio.run(main(query))
