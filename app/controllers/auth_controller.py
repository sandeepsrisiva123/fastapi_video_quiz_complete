
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.user_service import UserService
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    svc = UserService(db)
    user = svc.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access = create_access_token({"sub": str(user.id), "role": user.role.value, "userName":user.useranme})
    refresh = create_refresh_token({"sub": str(user.id), "role": user.role.value, "userName":user.username})
    svc.save_refresh_token(user.id, refresh)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

@router.post("/refresh")
def refresh_token(payload: dict = Body(...), db: Session = Depends(get_db)):
    token = payload.get("refresh_token")
    if not token:
        raise HTTPException(status_code=400, detail="Missing refresh_token")
    svc = UserService(db)
    dbt = svc.validate_refresh_token(token)
    if not dbt:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
    data = decode_token(token)
    new_access = create_access_token({"sub": data.get("sub"), "role": data.get("role")})
    return {"access_token": new_access, "token_type": "bearer"}

@router.post("/logout")
def logout(payload: dict = Body(...), db: Session = Depends(get_db)):
    token = payload.get("refresh_token")
    if not token:
        raise HTTPException(status_code=400, detail="Missing refresh_token")
    svc = UserService(db)
    revoked = svc.revoke_refresh_token(token)
    if not revoked:
        raise HTTPException(status_code=400, detail="Token not found")
    return {"msg": "Logged out"}
