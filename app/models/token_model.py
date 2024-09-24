from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from app.db.postgres_database import Base
from datetime import datetime, timezone

class Token(Base):
    __tablename__ = "tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    client_id = Column(String, index=True)
    client_name = Column(String(50), index=True)
    role = Column(String(50))
    is_active = Column(Boolean)
    expires_at = Column(Integer)
    token = Column(String, index=True)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))