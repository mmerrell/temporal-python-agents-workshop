"""solution/run_worker.py — reference implementation"""
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflow import WeatherAgentWorkflow
from activities import call_llm, get_weather_alerts


async def main():
    client = await Client.connect("localhost:7233")
    async with Worker(
        client,
        task_queue="weather-agent",
        workflows=[WeatherAgentWorkflow],
        activities=[call_llm, get_weather_alerts],
    ):
        print("Worker started. Listening on task queue: weather-agent")
        print("Press Ctrl+C to stop.\n")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
