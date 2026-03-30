"""
Start a worker for the durable SDK agent.

Usage:
    python run_worker.py
"""

import asyncio

from temporalio.client import Client
from temporalio.contrib.openai_agents import OpenAIAgentsPlugin
from temporalio.worker import Worker

from activities import get_coordinates, get_distance_km, get_weather_alerts
from workflow import WeatherAgentWorkflow


async def main():
    client = await Client.connect(
        "127.0.0.1:7233",
        plugins=[OpenAIAgentsPlugin()],
    )

    worker = Worker(
        client,
        task_queue="weather-agent-sdk",
        workflows=[WeatherAgentWorkflow],
        activities=[get_weather_alerts, get_coordinates, get_distance_km],
    )

    print("Worker started. Ctrl+C to stop.")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
