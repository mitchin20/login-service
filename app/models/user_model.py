from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from app.db.postgres_database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String(50), index=True)
    lastName = Column(String(50), index=True)
    email = Column(String(120), index=True)
    password = Column(String) # encrypted password
    role = Column(String(50), index=True)
    isActive = Column(Boolean, index=True)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))