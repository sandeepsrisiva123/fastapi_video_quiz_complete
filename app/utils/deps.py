
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.core.security import decode_token
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from sqlalchemy import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        sub = payload.get("sub")
        role = payload.get("role")
        if not sub or not role:
            raise ValueError('invalid token')
        user = db.scalar(select(User).where(User.id == int(sub)))
        if not user:
            raise ValueError('user not found')
        return {"id": user.id, "role": user.role.value, "username": user.username}
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

def require_role(allowed: list):
    def checker(current=Depends(get_current_user)):
        if current['role'] not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Insufficient permissions')
        return current
    return checker
