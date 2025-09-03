
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    role: str = "student"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True
