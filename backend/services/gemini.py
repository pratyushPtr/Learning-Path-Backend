# Import json module for parsing JSON responses from the LLM
import json

# Import the genai client library for interacting with Google's Gemini API
from google import genai

# Import types module for configuring the API request parameters
from google.genai import types

# Import the QuizResponse and LearningPathResponse schemas for type validation
from models.schemas import QuizResponse, LearningPathResponse

# Initialize the global client variable (set to None initially)
client = None

# Define the Gemini model name to use for all API calls
MODEL_NAME = "gemini-2.5-flash-lite"

# Configure the Gemini LLM API with the provided API key
def configure_gemini(api_key: str):
    global client
    client = genai.Client(api_key=api_key)

# Generate a learning path based on user input parameters
def generate_learning_path(goal: str, experience_level: str, hours_per_week: int) -> dict:
    # Create a prompt for the LLM to generate a learning path
    prompt = f"""
    You are a learning path expert.

    Create a step-by-step learning roadmap for someone who wants to: {goal}
    Their experience level is: {experience_level}
    They have {hours_per_week} hours per week to dedicate.
    Generate a 12-week layout.
    """

    # Call the Gemini API to generate the learning path
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=LearningPathResponse,
        ),
    )
    # Parse the JSON response and return it as a dictionary
    return json.loads(response.text)

# Generate a quiz for a specific milestone and week
def generate_quiz(milestone: str, week_number: int) -> dict:
    # Create a prompt for the LLM to generate quiz questions
    prompt = f"Generate a quiz with 3 multiple choice and 2 free response questions for: Week {week_number}: {milestone}"
    
    # Call the Gemini API to generate the quiz
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=QuizResponse,
        ),
    )
    # Parse the JSON response and return it as a dictionary
    return json.loads(response.text)

# Grade a quiz submission based on user answers
def grade_quiz(milestone: str, week_number: int, questions: list, answers: list) -> dict:
    # Build a block of text containing all questions and answers for grading
    qa_block = ""
    for q in questions:
        # Get the user's answer for this question
        answer = next((a["answer"] for a in answers if a["question_number"] == q["question_number"]), "No answer")
        # Format the options for display
        options = "\n".join(q["options"]) if q.get("options") else "Open ended"
        # Append the question and answer to the block
        qa_block += f"\nQuestion {q['question_number']} ({q['type']}): {q['question']}\nOptions: {options}\nUser's Answer: {answer}\n---"

    # Create a prompt for the LLM to grade the quiz
    prompt = f"""
    You are grading a quiz for someone learning {milestone} (Week {week_number})

    Here are their answers:
    {qa_block}

    Grade each answer. For multiple choice: mark correct only if they selected the right option.
    For open ended: use your judgment, partial credit is fine, reflect that in score.
    Pass threshold is 60%.
    """
    
    # Call the Gemini API to grade the quiz
    # Define a simple explicit schema structure inline or via a placeholder schema in models if preferred. 
    # For now, requesting json output mode for grading:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )
    # Parse the JSON response and return it as a dictionary
    return json.loads(response.text)
