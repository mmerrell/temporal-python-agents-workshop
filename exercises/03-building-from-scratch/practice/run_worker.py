"""
Start a worker that listens for WeatherAgentWorkflow tasks.

Usage:
    python run_worker.py
"""

import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import call_llm, get_coordinates, get_distance_km, get_weather_alerts
from workflow import WeatherAgentWorkflow


async def main():
    client = await Client.connect("127.0.0.1:7233")

    worker = Worker(
        client,
        task_queue="weather-agent",
        workflows=[WeatherAgentWorkflow],
        activities=[call_llm, get_weather_alerts, get_coordinates, get_distance_km],
    )

    print("Worker started. Ctrl+C to stop.")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
