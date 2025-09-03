
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.video import VideoCreate, VideoResponse
from app.services.video_service import VideoService
from app.utils.deps import require_role, get_current_user

router = APIRouter(prefix="/videos", tags=["videos"])

@router.post("/", response_model=VideoResponse, dependencies=[Depends(require_role(["admin","teacher"]))])
def create_video(payload: VideoCreate, db: Session = Depends(get_db), current=Depends(get_current_user)):
    service = VideoService(db)
    v = service.create(payload.title, payload.url, current['id'])
    return v

@router.get("/", response_model=list[VideoResponse], dependencies=[Depends(require_role(["admin","teacher","student"]))])
def list_videos(db: Session = Depends(get_db)):
    service = VideoService(db)
    return service.list()

@router.get("/{video_id}", response_model=VideoResponse, dependencies=[Depends(require_role(["admin","teacher","student"]))])
def get_video(video_id: int, db: Session = Depends(get_db)):
    service = VideoService(db)
    v = service.get(video_id)
    if not v:
        raise HTTPException(status_code=404, detail="Not found")
    return v
