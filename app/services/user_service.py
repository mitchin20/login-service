import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.lib.auth import create_access_token, verify_password
from datetime import timedelta

# Load environment variables from .env
load_dotenv()

# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET")
AGL = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 120

# Authentication the user
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

# Login service to handle login logic
def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Email or Password",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    # Create JWT token for the user
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
    
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }