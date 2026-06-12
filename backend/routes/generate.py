from fastapi import APIRouter
from models.schemas import LearningPathRequest, LearningPathResponse
from services.llm_client import generate_learning_path

router = APIRouter(tags=["Learning Path"])

@router.post("/generate", response_model=LearningPathResponse)
def generate_path(request: LearningPathRequest):
    result = generate_learning_path(
        goal=request.goal,
        experience_level=request.experience_level,
        hours_per_week=request.hours_per_week
    )
    return result