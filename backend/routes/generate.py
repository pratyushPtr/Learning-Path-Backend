# Import APIRouter from FastAPI for creating route handlers
from fastapi import APIRouter

# Import the LearningPathRequest and LearningPathResponse schemas from models
from models.schemas import LearningPathRequest, LearningPathResponse

# Import the generate_learning_path function from services
from services.gemini import generate_learning_path

# Create an API router for learning path generation endpoints
router = APIRouter(tags=["Learning Path"])

# POST endpoint to generate a learning path based on user input
@router.post("/generate", response_model=LearningPathResponse)
def generate_path(request: LearningPathRequest):
    # Call the generate_learning_path function with the request parameters
    result = generate_learning_path(
        goal=request.goal,
        experience_level=request.experience_level,
        hours_per_week=request.hours_per_week
    )
    # Return the generated learning path to the client
    return result
