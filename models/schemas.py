from pydantic import BaseModel

class LearningPathRequest(BaseModel):
    goal: str
    experience_level: str
    hours_per_week: int