import os
from fastapi import HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from passlib.context import CryptContext

# Load environment variables from .env
load_dotenv()

# Create a password context for hashing and verifying passwords 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify a password against a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET")
AGL = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 30 # default expiration time
SLIDING_EXPIRATION_THRESHOLD_MINUTES = 5 # if less than 5 minutes, extend token

# Create access token
def create_access_token(data: dict):
    to_encode = data.copy()

    # Token expire time
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=AGL)

    return encoded_jwt

# Sliding expiration approach
# Verify token and optionally extend its expiration
def verify_and_extend_token(token: str):
    try:
        # Decode token to verify it expiration time
        payload = jwt.decode(token, JWT_SECRET, algorithms=[AGL])
        expirationTime = payload.get("exp")

        if expirationTime is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has no expiration")
        
        # Convert unix timestamp to UTC format
        expiration_datetime = datetime.fromtimestamp(expirationTime, tz=timezone.utc)
        
        # check if token is expired
        if expiration_datetime < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

        # Implement sliding expiration: if the token is about to expire, renew it
        time_left = expiration_datetime - datetime.now(timezone.utc)
        if time_left.total_seconds() / 60 < SLIDING_EXPIRATION_THRESHOLD_MINUTES:
            # Token is about to expire, extend its expiration
            new_expiration = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
            payload["exp"] = new_expiration.timestamp()
            # Re-encode the token with the new expiration time
            renewed_token = jwt.encode(payload, JWT_SECRET, algorithm=AGL)
            return {"token": renewed_token, "extended": True}
        
        # If no extension is needed, return the original token
        return {"token": token, "extended": False}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

# Verify JWT Token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[AGL])
        return payload
    except JWTError:
        return None