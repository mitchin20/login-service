import logging
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.routers import auth_router
from app.routers import verify_token
from app.middlewares.token_validation_middleware import TokenValidationMiddleware
from app.db.postgres_database import database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lifespan handler: Manages the lifecycle of the app, handling startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Connecting to DB")
    # startup db connection
    await database.connect()

    yield
    
    logger.info(f"Disconnect DB")
    # shutdown db connection
    await database.disconnect()
    
app = FastAPI(lifespan=lifespan)

# root route
@app.get("/")
def read_root():
    try:
        return {"message": "Login Service"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# routes
app.include_router(auth_router.router)
app.include_router(verify_token.router)

# middleware
app.add_middleware(TokenValidationMiddleware)