from sqlalchemy import String, ForeignKey, Text, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    video_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("videos.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relationships
    video = relationship("Video", back_populates="quizzes")
    questions = relationship(
        "Question",
        back_populates="quiz",
        cascade="all, delete-orphan"
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    quiz_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("quizzes.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship(
        "Option",
        back_populates="question",
        cascade="all, delete-orphan"
    )


class Option(Base):
    __tablename__ = "options"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    question_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relationships
    question = relationship("Question", back_populates="options")
