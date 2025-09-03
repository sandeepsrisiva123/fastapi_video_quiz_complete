
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.db.session import get_db
from app.services.user_service import UserService as Svc
from app.utils.deps import get_current_user, require_role

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/signup", response_model=UserResponse)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    if payload.role in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Only admin can create teacher/admin")
    svc = Svc(db)
    user = svc.create_user(payload.username, payload.password, payload.role)
    return user

@router.post("/create", response_model=UserResponse, dependencies=[Depends(require_role(["admin"]))])
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    svc = Svc(db)
    user = svc.create_user(payload.username, payload.password, payload.role)
    return user

@router.get("/me", response_model=UserResponse)
def me(current=Depends(get_current_user), db: Session = Depends(get_db)):
    svc = Svc(db)
    user = svc.get_by_username(current['username'])
    return user

@router.get("/", dependencies=[Depends(require_role(["admin"]))])
def list_users(db: Session = Depends(get_db)):
    svc = Svc(db)
    return db.query(type(svc).db.__class__).all()  # placeholder - admin can implement listing
