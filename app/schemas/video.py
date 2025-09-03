
from pydantic import BaseModel
from typing import List, Optional
from app.schemas.quiz import QuizResponse

class VideoBase(BaseModel):
    title: str
    url: str

class VideoCreate(VideoBase):
    pass

class VideoResponse(VideoBase):
    id: int
    owner_id: Optional[int] = None
    quizzes: List[QuizResponse] = []
    class Config:
        from_attributes = True
