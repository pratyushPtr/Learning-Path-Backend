import json
from google import genai

client = None

def configure_gemini(api_key: str):
    global client
    client = genai.Client(api_key=api_key)

def generate_learning_path(goal: str, experience_level: str, hours_per_week: int) -> dict:
    prompt = f"""
    You are a learning path expert.

    Create a step-by-step learning roadmap for someone who wants to: {goal}
    Their experience level is: {experience_level}
    They have {hours_per_week} hours per week to dedicate.

    Respond ONLY with a valid JSON object. No markdown, no explanation, no backticks.
    Use exactly this structure:

    {{
      "goal": "{goal}",
      "experience_level": "{experience_level}",
      "hours_per_week": {hours_per_week},
      "total_weeks": 12,
      "weeks": [
        {{
          "week": 1,
          "milestone": "short description of the goal for this week",
          "resources": ["resource 1", "resource 2"],
          "checkpoint": "how to assess progress this week"
        }}
      ]
    }}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    raw = response.text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw)