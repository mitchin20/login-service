from fastapi import FastAPI
from app.routers import auth_router
from app.routers import verify_token
from app.middlewares.token_validation_middleware import TokenValidationMiddleware

app = FastAPI()

# root route
@app.get("/")
def read_root():
    return {"message": "Login Service"}

# middleware
app.add_middleware(TokenValidationMiddleware)

# routes
app.include_router(auth_router.router)
app.include_router(verify_token.router)
