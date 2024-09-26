from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_schema import UserLogin
from sqlalchemy.orm import Session
from app.db.postgres_database import get_db
from app.services.user_service import login_user

router = APIRouter()

# Login endpoint
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    try:
        return login_user(db, data.email, data.password)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
