
from pydantic import BaseModel
from typing import List, Optional
from app.schemas.option import OptionResponse

class OptionCreate(BaseModel):
    text: str
    is_correct: bool = False

class OptionResponse(BaseModel):
    id: int
    text: str
    is_correct: bool
    question_id: int
    class Config:
        from_attributes = True

class QuestionCreate(BaseModel):
    prompt: str
    options: List[OptionCreate]

class QuestionResponse(BaseModel):
    id: int
    prompt: str
    options: List[OptionResponse] = []
    class Config:
        from_attributes = True

class QuizCreate(BaseModel):
    title: str
    video_id: int
    questions: List[QuestionCreate]

class QuizResponse(BaseModel):
    id: int
    title: str
    video_id: int
    questions: List[QuestionResponse] = []
    class Config:
        from_attributes = True
