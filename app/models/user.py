from sqlalchemy import String, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from app.db.base import Base


class RoleEnum(PyEnum):
    admin = "admin"
    teacher = "teacher"
    student = "student"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(
        Enum(RoleEnum, name="role_enum"),
        nullable=False,
        default=RoleEnum.student,
    )

    # Relationships
    refresh_tokens = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    videos = relationship(
        "Video",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
