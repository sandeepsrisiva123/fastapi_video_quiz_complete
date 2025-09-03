
from sqlalchemy.orm import Session
from app.models.video import Video

class VideoService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, title: str, url: str, owner_id: int):
        video = Video(title=title, url=url, owner_id=owner_id)
        self.db.add(video)
        self.db.commit()
        self.db.refresh(video)
        return video

    def list(self):
        return self.db.query(Video).all()

    def get(self, video_id: int):
        return self.db.query(Video).filter(Video.id == video_id).first()
