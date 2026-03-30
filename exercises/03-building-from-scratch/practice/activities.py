"""
Activities for the weather agent.

Activities handle all I/O: LLM calls, tool calls, external APIs.
They have no knowledge of the agentic loop — that separation is intentional.
"""

import json
import httpx
from openai import AsyncOpenAI
from temporalio import activity

client = AsyncOpenAI()

# Tool definitions — what the LLM can call
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather_alerts",
            "description": "Get active weather alerts for a US state. Returns NWS alerts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "Two-letter US state code (e.g. CA, TX, NY)",
                    }
                },
                "required": ["state"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_coordinates",
            "description": "Get the latitude and longitude for a location name or address.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location name, address, or city",
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_distance_km",
            "description": "Calculate the straight-line distance between two lat/lon coordinates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat1": {"type": "number"},
                    "lon1": {"type": "number"},
                    "lat2": {"type": "number"},
                    "lon2": {"type": "number"},
                },
                "required": ["lat1", "lon1", "lat2", "lon2"],
            },
        },
    },
]


@activity.defn
async def call_llm(messages: list, tools: list) -> dict:
    """Call the LLM. Returns the raw API response as a dict."""
    activity.logger.info(f"Calling LLM with {len(messages)} messages")
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    return response.model_dump()


@activity.defn
async def get_weather_alerts(state: str) -> str:
    """Fetch active weather alerts for a US state from the National Weather Service."""
    activity.logger.info(f"Fetching weather alerts for: {state}")
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


@activity.defn
async def get_coordinates(location: str) -> dict:
    """Get latitude/longitude for a location using the Nominatim geocoding API."""
    activity.logger.info(f"Getting coordinates for: {location}")
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


@activity.defn
async def get_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> dict:
    """Calculate straight-line distance between two lat/lon points."""
    import math
    activity.logger.info(f"Calculating distance ({lat1},{lon1}) -> ({lat2},{lon2})")
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
