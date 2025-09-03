
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.controllers import auth_controller, user_controller, video_controller, quiz_controller

app = FastAPI(title="Video & Quiz Service")

# create tables for dev if needed
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SecurityHeadersMiddleware)

app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(video_controller.router)
app.include_router(quiz_controller.router)

@app.get("/")
def root():
    return {"ok": True}
