from pydantic import BaseModel

class LearningPathRequest(BaseModel):
    goal: str
    experience_level: str
    hours_per_week: int

class QuizRequest(BaseModel):
    milestone: str
    week_number: int

class QuizQuestion(BaseModel):
    question_number: int
    type: str
    question: str
    options: list[str] | None = None

class QuizResponse(BaseModel):
    week_number: int
    milestone: str
    questions: list[QuizQuestion]

class QuizAnswer(BaseModel):
    question_number: int
    answer: str

class QuizSubmission(BaseModel):
    week_number: int
    milestone: str
    questions: list[QuizQuestion]
    answers: list[QuizAnswer]




