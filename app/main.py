from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import auth_router
from app.routers import verify_token
from app.middlewares.token_validation_middleware import TokenValidationMiddleware
from app.db.postgres_database import database

# Lifespan handler: Manages the lifecycle of the app, handling startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup db connection
    await database.connect()

    yield
    
    # shutdown db connection
    await database.disconnect()
    
app = FastAPI(lifespan=lifespan)

# root route
@app.get("/")
def read_root():
    return {"message": "Login Service"}

# middleware
app.add_middleware(TokenValidationMiddleware)

# routes
app.include_router(auth_router.router)
app.include_router(verify_token.router)