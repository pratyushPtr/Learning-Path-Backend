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

def generate_quiz(milestone: str, week_number: int) -> dict:
    prompt = f"""
    You are a quiz generator for a learning platform

    Generate a quiz for someone who just completed this weekly milestone:
    Week {week_number}: {milestone}

    Respond ONLY with a valid JSON object. No markdowns, no explanations, no backticks.
    Please use the following structure when responding:

    {{
      "week_number": {week_number}, 
      "milestone": "{milestone}", 
      "questions": [
        {{
          "question_number": 1, 
          "type": "multiple_choice", 
          "question": "question text here", 
          "options": ["A. option1", "B. option2", "C. option3", "D. option4"]
        }},
        {{
          "question_number": 2, 
          "type": "multiple_choice", 
          "question": "question text here", 
          "options": ["A. option1", "B. option2", "C. option3", "D. option4"]
        }},
        {{
          "question_number": 3, 
          "type": "multiple_choice", 
          "question: "question text here", 
          "options": ["A. option1", "B. option2", "C. option3", "D. option4"]
        }},
        {{
          "question_number": 4, 
          "type": "free_response", 
          "question": "question text here", 
          "options": null
        }},
        {{
          "question_number": 5, 
          "type": "free_response", 
          "question": "question text here", 
          "options": null
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

def grade_quiz(milestone: str, week_number: int, questions: list, answers: list) -> dict:
    qa_block = ""
    for q in questions:
        answer = next((a["answer"] for a in answers if a["question_number"] == q["question_number"]), "No answer")
        options = "\n".join(q["options"]) if q.get("options") else "Open ended"
        qa_block += f"""
        Question {q["question_number"]} ({q["type"]}): {q["question"]}
        Options: {options}
        User's Answer: {answer}
        ---"""


    prompt = f"""
    You are grading a quiz for someone learning {milestone} (Week {week_number})

    Here are thier answers:
    {qa_block}

    Grade each answer and respond only with a valid JSON object, No markdowns, no explanations, no backticks.
    Please use the following structure when responding:

    {{
      "week_number": {week_number},
      "score": 4, 
      "total": 5, 
      "passed": true, 
      "feedback": [
        {{
          "question_number": 1, 
          "correct": true, 
          "explanation": "brief explanation"
        }}
      ],
      "overall_feedback": "one sentence summary of performance"
    }}

    For multiple choice: mark correct only if they selected the right option.
    For open ended: use your judgment, partial credit is fine, reflect that in score.
    Pass threshold is 60%.
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




        


  
