"""
Exercise 04a: The same weather agent rebuilt with the OpenAI Agents SDK.
No Temporal yet — this is the "raw" version.

Notice how little code there is compared to Exercise 03. The SDK handles:
  - The agentic loop
  - Tool call parsing
  - Context management (conversation history)

The tradeoff: if this process dies, everything is lost.
Run with: python agent_raw.py "What are the weather alerts in California?"
"""

import asyncio
import sys

import httpx
from agents import Agent, Runner, function_tool


@function_tool
async def get_weather_alerts(state: str) -> str:
    """Get active weather alerts for a US state. Use two-letter state code e.g. CA, TX, NY."""
    url = f"https://api.weather.gov/alerts/active?area={state.upper()}"
    async with httpx.AsyncClient() as http:
        resp = await http.get(url, headers={"User-Agent": "temporal-agent-workshop"})
        if resp.status_code != 200:
            return f"Could not retrieve alerts for {state} (status {resp.status_code})"
        data = resp.json()
        alerts = data.get("features", [])
        if not alerts:
            return f"No active weather alerts for {state}."
        summaries = []
        for alert in alerts[:5]:
            props = alert.get("properties", {})
            summaries.append(
                f"- {props.get('event', 'Alert')}: {props.get('headline', 'No details')}"
            )
        return "\n".join(summaries)


@function_tool
async def get_coordinates(location: str) -> dict:
    """Get the latitude and longitude for a location name or address."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": location, "format": "json", "limit": 1}
    async with httpx.AsyncClient() as http:
        resp = await http.get(
            url, params=params, headers={"User-Agent": "temporal-agent-workshop"}
        )
        results = resp.json()
        if not results:
            return {"error": f"Could not find coordinates for: {location}"}
        return {
            "lat": float(results[0]["lat"]),
            "lon": float(results[0]["lon"]),
            "display_name": results[0]["display_name"],
        }


@function_tool
async def get_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> dict:
    """Calculate the straight-line distance in km between two lat/lon coordinates."""
    import math
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    distance = 2 * R * math.asin(math.sqrt(a))
    return {
        "distance_km": round(distance, 2),
        "distance_miles": round(distance * 0.621371, 2),
    }


agent = Agent(
    name="Weather Agent",
    instructions=(
        "You are a helpful assistant that answers questions about weather alerts "
        "and distances between locations. Use your tools to look up real data."
    ),
    tools=[get_weather_alerts, get_coordinates, get_distance_km],
)


async def main(query: str):
    print(f"\nQuery: {query}\n")
    result = await Runner.run(agent, query)
    print(f"Result:\n{result.final_output}")


if __name__ == "__main__":
    query = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "What are the active weather alerts in California?"
    )
    asyncio.run(main(query))
