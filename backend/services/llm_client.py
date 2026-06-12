import json
import logging
import os
import time
from google.genai import types

from google import genai
import google.genai
from dotenv import load_dotenv
from services import cache

load_dotenv()
logger = logging.getLogger(__name__)

MODEL_NAME = "gemini-2.5-flash-lite"
MAX_RETRIES = 3
BASE_DELAY = 2

class LLMError(Exception):
    """Raised when the Gemini API service fails after retries."""

def _get_client():
    """Lazily initialize the client only when needed, avoiding startup crashes."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")
    return genai.Client(api_key=api_key)

MAX_RETRIES = 3
BASE_DELAY = 2

class LLMError(Exception):
    """Raised when the Gemini API service fails after retries."""

def _call_gemini_structured(prompt: str, response_schema: type) -> dict:
    """Helper function to make type-safe structured JSON calls to Gemini."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # Call the lazy initializer here
            client = _get_client()
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=response_schema,
                    temperature=0.3,
                ),
            )
            return json.loads(response.text.strip())
        except Exception as e:
            logger.warning("Gemini call retry %s/%s failed: %s", attempt, MAX_RETRIES, e)
            if attempt == MAX_RETRIES:
                raise LLMError(f"Gemini API service error: {e}")
            time.sleep(BASE_DELAY * attempt)

def _near_threshold(score: int, total: int) -> bool:
    if total == 0:
        return False
    return 55 <= (score / total) * 100 <= 65

def generate_learning_path(goal: str, experience_level: str, hours_per_week: int) -> dict:
    cache_key = cache.make_key("path", goal=goal.lower().strip(), experience_level=experience_level, hours_per_week=hours_per_week)
    if (cached := cache.get(cache_key)) is not None:
        return cached

    prompt = f"""
    Create a highly structured step-by-step 12-week learning roadmap for someone who wants to learn: {goal}
    Their experience level is: {experience_level}
    They have {hours_per_week} hours per week to dedicate.
    """
    
    # Inline structural validation schema mapping to LearningPathResponse requirements
    schema = {
        "type": "OBJECT",
        "properties": {
            "goal": {"type": "STRING"},
            "experience_level": {"type": "STRING"},
            "hours_per_week": {"type": "INTEGER"},
            "total_weeks": {"type": "INTEGER"},
            "weeks": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "week": {"type": "INTEGER"},
                        "milestone": {"type": "STRING"},
                        "resources": {"type": "ARRAY", "items": {"type": "STRING"}},
                        "checkpoint": {"type": "STRING"}
                    },
                    "required": ["week", "milestone", "resources", "checkpoint"]
                }
            }
        },
        "required": ["goal", "experience_level", "hours_per_week", "total_weeks", "weeks"]
    }

    result = _call_gemini_structured(prompt, schema)
    cache.set(cache_key, result)
    return result

def generate_quiz(milestone: str, week_number: int) -> dict:
    cache_key = cache.make_key("quiz", milestone=milestone.lower().strip(), week_number=week_number)
    if (cached := cache.get(cache_key)) is not None:
        return cached

    prompt = f"""
    Generate a quiz with exactly 3 multiple choice and 2 free response questions to assess this milestone:
    Week {week_number}: {milestone}
    """
    
    schema = {
        "type": "OBJECT",
        "properties": {
            "week_number": {"type": "INTEGER"},
            "milestone": {"type": "STRING"},
            "questions": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "question_number": {"type": "INTEGER"},
                        "type": {"type": "STRING"},
                        "question": {"type": "STRING"},
                        "options": {"type": "ARRAY", "items": {"type": "STRING"}, "nullable": True}
                    },
                    "required": ["question_number", "type", "question"]
                }
            }
        },
        "required": ["week_number", "milestone", "questions"]
    }

    result = _call_gemini_structured(prompt, schema)
    cache.set(cache_key, result)
    return result

def grade_quiz(milestone: str, week_number: int, questions: list, answers: list) -> dict:
    qa_block = ""
    for q in questions:
        answer = next((a["answer"] for a in answers if a["question_number"] == q["question_number"]), "No answer")
        options = "\n".join(q["options"]) if q.get("options") else "Open ended"
        qa_block += f"\nQuestion {q['question_number']}: {q['question']}\nOptions: {options}\nUser: {answer}\n---"

    prompt = f"""
    Grade this quiz submission for milestone: {milestone} (Week {week_number}).
    User Answers:
    {qa_block}
    
    Pass threshold is 60%.
    """
    
    schema = {
        "type": "OBJECT",
        "properties": {
            "week_number": {"type": "INTEGER"},
            "score": {"type": "INTEGER"},
            "total": {"type": "INTEGER"},
            "passed": {"type": "BOOLEAN"},
            "feedback": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "question_number": {"type": "INTEGER"},
                        "correct": {"type": "BOOLEAN"},
                        "explanation": {"type": "STRING"}
                    },
                    "required": ["question_number", "correct", "explanation"]
                }
            },
            "overall_feedback": {"type": "STRING"}
        },
        "required": ["week_number", "score", "total", "passed", "feedback", "overall_feedback"]
    }

    result = _call_gemini_structured(prompt, schema)
    
    # Near pass/fail threshold — re-grade for better accuracy
    if _near_threshold(result.get("score", 0), result.get("total", 5)):
        logger.info("Score near threshold, re-grading for better accuracy.")
        result = _call_gemini_structured(prompt, schema)
        
    return result