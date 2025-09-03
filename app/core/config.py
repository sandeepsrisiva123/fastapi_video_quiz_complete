
from pydantic_settings import BaseSettings
from typing import List, Any
from pydantic import AnyHttpUrl
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    CORS_ORIGINS: List[AnyHttpUrl] | List[str] = []
    ENV: str = os.getenv("ENV","dev")

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
