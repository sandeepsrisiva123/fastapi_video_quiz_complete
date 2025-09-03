
from sqlalchemy.orm import Session
from app.models.user import User, RoleEnum
from app.models.refresh_token import RefreshToken
from app.core.security import hash_password, verify_password
from typing import Optional
from datetime import datetime

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, username: str, password: str, role: str) -> User:
        if self.get_by_username(username):
            raise ValueError("username exists")
        user = User(username=username, password=hash_password(password), role=RoleEnum(role))
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate(self, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(username)
        if user and verify_password(password, user.password):
            return user
        return None

    def save_refresh_token(self, user_id: int, token: str) -> RefreshToken:
        db_token = RefreshToken(user_id=user_id, token=token, expires_at=RefreshToken.get_expiry(), revoked=False)
        self.db.add(db_token)
        self.db.commit()
        self.db.refresh(db_token)
        return db_token

    def revoke_refresh_token(self, token: str):
        db_token = self.db.query(RefreshToken).filter(RefreshToken.token == token).first()
        if db_token:
            db_token.revoked = True
            self.db.commit()
        return db_token

    def validate_refresh_token(self, token: str):
        db_token = self.db.query(RefreshToken).filter(RefreshToken.token == token, RefreshToken.revoked == False).first()
        if not db_token:
            return None
        if db_token.expires_at < datetime.utcnow():
            return None
        return db_token
