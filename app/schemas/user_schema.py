from pydantic import BaseModel, EmailStr

# Pydantic schema for login request
class UserLogin(BaseModel):
    email: EmailStr
    password: str