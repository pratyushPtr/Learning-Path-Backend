from typing import Literal
from pydantic import BaseModel, Field

# LearningPathRequest model - input schema for generating a learning path
class LearningPathRequest(BaseModel):
    # The learning goal the user wants to achieve
    goal: str
    
    # The user's experience level (must be one of the three options)
    experience_level: Literal["beginner", "intermediate", "advanced"]
    
    # Hours per week available for learning (must be between 1 and 40)
    hours_per_week: int = Field(gt=0, le=40)

# QuizRequest model - input schema for generating a quiz
class QuizRequest(BaseModel):
    # The milestone being tested
    milestone: str
    
    # Week number for the quiz (must be between 1 and 12)
    week_number: int = Field(ge=1, lr=12)

# QuizQuestion model - represents a single question in a quiz
class QuizQuestion(BaseModel):
    # The question number (1-based index)
    question_number: int
    
    # The type of question (e.g., "multiple_choice", "free_response")
    type: str
    
    # The actual question text
    question: str
    
    # List of answer options for multiple choice questions (None for free response)
    options: list[str] | None = None

# QuizResponse model - output schema from the LLM for quiz generation
class QuizResponse(BaseModel):
    # The week number this quiz belongs to
    week_number: int
    
    # The milestone being tested
    milestone: str
    
    # List of questions in the quiz
    questions: list[QuizQuestion]

# QuizAnswer model - represents a user's answer to a question
class QuizAnswer(BaseModel):
    # The question number this answer corresponds to
    question_number: int
    
    # The user's answer text
    answer: str

# QuizSubmission model - input schema for submitting a quiz
class QuizSubmission(BaseModel):
    # Week number for the submission (must be between 1 and 12)
    week_number: int = Field(ge=1, le=12)
    
    # The milestone being tested
    milestone: str
    
    # List of questions in the quiz
    questions: list[QuizQuestion]
    
    # List of user's answers
    answers: list[QuizAnswer]

# WeekMilestone model - represents a single week in the learning path
class WeekMilestone(BaseModel):
    # Week number
    week: int
    
    # The milestone/goal for this week
    milestone: str
    
    # List of resources for this week
    resources: list[str]
    
    # Checkpoint or assessment for this week
    checkpoint: str

# LearningPathResponse model - output schema from the LLM for learning path generation
class LearningPathResponse(BaseModel):
    # The learning goal
    goal: str
    
    # The user's experience level
    experience_level: str
    
    # Hours per week available for learning
    hours_per_week: int
    
    # Total number of weeks in the learning path
    total_weeks: int
    
    # List of weeks with their milestones and resources
    weeks: list[WeekMilestone]
