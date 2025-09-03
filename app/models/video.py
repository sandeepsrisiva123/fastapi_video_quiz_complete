from sqlalchemy import String, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)

    owner_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    owner = relationship("User", back_populates="videos")
    quizzes = relationship(
        "Quiz",
        back_populates="video",
        cascade="all, delete-orphan"
    )
