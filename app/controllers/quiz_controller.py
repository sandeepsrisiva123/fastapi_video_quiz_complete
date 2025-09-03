
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.quiz import QuizCreate, QuizResponse, QuestionCreate
from app.services.quiz_service import QuizService
from app.utils.deps import require_role

router = APIRouter(prefix="/quizzes", tags=["quizzes"])

@router.post("/", response_model=QuizResponse, dependencies=[Depends(require_role(["admin","teacher"]))])
def create_quiz(payload: QuizCreate, db: Session = Depends(get_db)):
    service = QuizService(db)
    q = service.create(payload.title, payload.video_id, [q.model_dump() for q in payload.questions])
    return q

@router.get("/by-video/{video_id}", response_model=list[QuizResponse], dependencies=[Depends(require_role(["admin","teacher","student"]))])
def by_video(video_id: int, db: Session = Depends(get_db)):
    service = QuizService(db)
    return service.get_by_video(video_id)

@router.post("/{quiz_id}/submit", dependencies=[Depends(require_role(["admin","teacher","student"]))])
def submit(quiz_id: int, payload: dict, db: Session = Depends(get_db)):
    answers = payload.get("answers", [])
    service = QuizService(db)
    try:
        total, correct = service.grade(quiz_id, answers)
    except ValueError:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return {"total": total, "correct": correct}
