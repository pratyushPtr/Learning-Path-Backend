# Import APIRouter from FastAPI for creating route handlers
from fastapi import APIRouter

# Import the QuizRequest and QuizSubmission schemas from models
from models.schemas import QuizRequest, QuizSubmission

# Import the generate_quiz and grade_quiz functions from services
from services.gemini import generate_quiz, grade_quiz

# Create an API router for quiz-related endpoints
router = APIRouter(tags=["Quiz Assessment"])

# POST endpoint to generate a quiz for a specific milestone and week
@router.post("/quiz/generate")
def get_quiz(request: QuizRequest):
    # Call the generate_quiz function with the request parameters
    result = generate_quiz(
        milestone=request.milestone,
        week_number=request.week_number
    )
    # Return the generated quiz to the client
    return result

# POST endpoint to submit and grade a quiz
@router.post("/quiz/submit")
def submit_quiz(submission: QuizSubmission):
    # Convert Pydantic models to dictionaries for the grading function
    result = grade_quiz(
        milestone=submission.milestone,
        week_number=submission.week_number,
        questions=[q.model_dump() for q in submission.questions],
        answers=[a.model_dump() for a in submission.answers]
    )
    # Return the grading result to the client
    return result
