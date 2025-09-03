
from pydantic import BaseModel

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
