from fastapi import APIRouter
from models.schemas import QuizRequest, QuizResponse, QuizSubmission, QuizSubmissionResponse
from services.llm_client import generate_quiz, grade_quiz

router = APIRouter(tags=["Quiz Assessment"])

@router.post("/quiz/generate", response_model=QuizResponse)
def get_quiz(request: QuizRequest):
    result = generate_quiz(
        milestone=request.milestone,
        week_number=request.week_number
    )
    return result

@router.post("/quiz/submit", response_model=QuizSubmissionResponse)
def submit_quiz(submission: QuizSubmission):
    result = grade_quiz(
        milestone=submission.milestone,
        week_number=submission.week_number,
        questions=[q.model_dump() if hasattr(q, "model_dump") else q.dict() for q in submission.questions],
        answers=[a.model_dump() if hasattr(a, "model_dump") else a.dict() for a in submission.answers]
    )
    return result