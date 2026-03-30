"""
Section 2: Building a Durable Agent from Scratch
practice/activities.py

Activities are the agent's hands — they handle all I/O.
They have no knowledge of the agentic loop. That separation is intentional.
"""

import httpx
from openai import AsyncOpenAI
from temporalio import activity

client = AsyncOpenAI()

# Tool definitions — what we tell the LLM it can call.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather_alerts",
            "description": (
                "Get active weather alerts for a US state. "
                "Returns current NWS alerts. Use the two-letter state code."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "Two-letter US state code, e.g. CA, TX, NY",
                    }
                },
                "required": ["state"],
            },
        },
    }
]


@activity.defn
async def call_llm(messages: list, tools: list) -> dict:
    """Call the LLM. Returns the raw API response serialized as a dict."""
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
        resp = await http.get(
            url, headers={"User-Agent": "temporal-agents-workshop"}
        )
        if resp.status_code != 200:
            return f"Could not retrieve alerts for {state} (HTTP {resp.status_code})"
        features = resp.json().get("features", [])
        if not features:
            return f"No active weather alerts for {state}."
        lines = []
        for f in features[:5]:
            props = f.get("properties", {})
            lines.append(f"- {props.get('event', 'Alert')}: {props.get('headline', '')}")
        return "\n".join(lines)
