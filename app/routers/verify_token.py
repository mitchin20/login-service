from fastapi import APIRouter
from pydantic import BaseModel
from app.lib.auth import verify_and_extend_token

router = APIRouter()

# request model
class TokenVerificationRequest(BaseModel):
    token: str
    
# response model
class TokenVerificationResponse(BaseModel):
    token: str
    extended: bool

@router.post("/verify-token")
def verify_token(request: TokenVerificationRequest):
    result = verify_and_extend_token(request.token)
    
    return TokenVerificationResponse(**result) # python ** unpacking