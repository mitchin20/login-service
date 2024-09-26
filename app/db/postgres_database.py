import os
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from databases import Database
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get env variable
DATABASE_URL = os.getenv("POSTGRES_URL")

# SQLAlchemy Base class
Base: DeclarativeMeta = declarative_base()

# Create an async database connection
database = Database(DATABASE_URL)

# Create a synchronous engine for migrations or operations
# Customize the connection pool size if needed
    # poolclass=QueuePool,      # Default pool class
    # pool_size=5,              # The size of the pool to maintain
    # max_overflow=10,          # Number of extra connections allowed when pool is full
    # pool_timeout=30,          # Time to wait for a connection before raising an error
    # pool_recycle=1800         # Timeout for recycling idle connections
engine = create_engine(DATABASE_URL, echo=True)

# Sessionmaker for interacting with the database synchronously
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency Injection for Database Session:
# open & close session automatically
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()