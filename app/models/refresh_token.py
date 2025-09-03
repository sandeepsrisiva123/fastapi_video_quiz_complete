from sqlalchemy import Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timedelta
from app.db.base import Base
from app.core.config import settings


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    token: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="refresh_tokens")

    @staticmethod
    def get_expiry() -> datetime:
        """Generate expiry datetime for a new refresh token."""
        return datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
