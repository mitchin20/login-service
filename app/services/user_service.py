import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.lib.auth import create_access_token, verify_password
from datetime import timedelta

# Load environment variables from .env
load_dotenv()

# Authentication the user
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

# exclude fields
def to_dict(self, exclude=None):
    exclude = exclude or []
    return {key: value for key, value in self.__dict__.items() if key not in exclude}

# Login service to handle login logic
def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Email or Password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user_without_password = to_dict(user, exclude=["password"])
        
    # Create JWT token for the user
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "user": user_without_password,
        "access_token": access_token,
        "token_type": "Bearer"
    }