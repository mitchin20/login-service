import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.postgres_database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User
from app.lib.auth import  hash_password

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the database dependency for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        
app.dependency_overrides[get_db] = override_get_db

# Create a test client
client = TestClient(app)

# Run this once before all tests to create tables
@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    
    # Pre-populate the test database with a user
    db = TestingSessionLocal()
    hashed_password = hash_password("123123")
    new_user = User(
        email="example@gmail.com",
        password=hashed_password,
        firstName="John",
        lastName="Smith",
        role="user",
        isActive=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    yield
    
    Base.metadata.drop_all(bind=engine)

# Test login endpoint
def test_login_success(setup_database):
    # Attempt to login with existing user
    login_response = client.post("/login", json={
        "email": "example@gmail.com",
        "password": "123123"
    })
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()