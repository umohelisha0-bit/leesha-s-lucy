"""Call and session models"""
from sqlalchemy import Column, String, DateTime, Boolean, Float, Integer, ForeignKey, JSON
from sqlalchemy.sql import func
from app.database import Base
import uuid


class Call(Base):
    """Call model for storing call information"""
    __tablename__ = "calls"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String(50), default="active")  # active, ended, failed
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Float, nullable=True)  # Unlimited - no duration limit
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Call {self.id}>"


class CallSession(Base):
    """Call session model for tracking active sessions"""
    __tablename__ = "call_sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    call_id = Column(String, ForeignKey("calls.id"), nullable=False, index=True)
    session_id = Column(String, unique=True, nullable=False, index=True)
    connection_id = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    video_enabled = Column(Boolean, default=True)
    audio_enabled = Column(Boolean, default=True)
    total_messages = Column(Integer, default=0)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    metadata = Column(JSON, nullable=True)
    
    def __repr__(self):
        return f"<CallSession {self.id}>"
