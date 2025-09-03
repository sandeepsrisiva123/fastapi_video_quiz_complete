
from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"

class TokenRefreshRequest(BaseModel):
    refresh_token: str
