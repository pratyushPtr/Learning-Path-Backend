from pydantic import BaseModel, Field
from typing import Literal

# --- REQUEST SCHEMAS (Inbound Data) ---

class LearningPathRequest(BaseModel):
    goal: str = Field(min_length=3)
    experience_level: Literal["beginner", "intermediate", "advanced"]
    hours_per_week: int = Field(ge=1, le=40)

class QuizRequest(BaseModel):
    milestone: str
    week_number: int = Field(ge=1, le=12)

class QuizQuestion(BaseModel):
    question_number: int
    type: str
    question: str
    options: list[str] | None = None

class QuizAnswer(BaseModel):
    question_number: int
    answer: str

class QuizSubmission(BaseModel):
    week_number: int
    milestone: str
    questions: list[QuizQuestion]
    answers: list[QuizAnswer]


# --- RESPONSE SCHEMAS (Outbound Data & Frontend Bindings) ---

class WeekMilestone(BaseModel):
    week: int
    milestone: str
    resources: list[str]
    checkpoint: str

class LearningPathResponse(BaseModel):
    goal: str
    experience_level: str
    hours_per_week: int
    total_weeks: int = 12
    weeks: list[WeekMilestone]

class QuizResponse(BaseModel):
    week_number: int
    milestone: str
    questions: list[QuizQuestion]

class FeedbackItem(BaseModel):
    question_number: int
    correct: bool
    explanation: str

class QuizSubmissionResponse(BaseModel):
    week_number: int
    score: int
    total: int
    passed: bool
    feedback: list[FeedbackItem]
    overall_feedback: str