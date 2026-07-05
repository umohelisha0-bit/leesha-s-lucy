"""Call management endpoints"""
import logging
import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Call, CallSession
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()


class CallRequest:
    """Request model for call creation"""
    user_id: str
    avatar_config: dict = None


@router.post("/start")
async def start_call(user_id: str, db: AsyncSession = Depends(get_db)):
    """
    Start a new video call session
    - No time limit
    - Unlimited duration
    """
    try:
        # Create new call
        call_id = str(uuid.uuid4())
        call = Call(
            id=call_id,
            user_id=user_id,
            status="active"
        )
        db.add(call)
        
        # Create call session
        session_id = str(uuid.uuid4())
        call_session = CallSession(
            id=str(uuid.uuid4()),
            call_id=call_id,
            session_id=session_id,
            is_active=True
        )
        db.add(call_session)
        await db.commit()
        
        logger.info(f"Call {call_id} started for user {user_id}")
        
        return {
            "call_id": call_id,
            "session_id": session_id,
            "status": "active",
            "started_at": datetime.utcnow().isoformat(),
            "features": {
                "unlimited_duration": True,
                "no_watermark": True,
                "emotion_detection": True,
                "avatar_customization": True
            }
        }
    except Exception as e:
        logger.error(f"Error starting call: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{call_id}")
async def get_call(call_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get call details
    """
    try:
        result = await db.execute(select(Call).where(Call.id == call_id))
        call = result.scalars().first()
        
        if not call:
            raise HTTPException(status_code=404, detail="Call not found")
        
        duration = None
        if call.ended_at:
            duration = (call.ended_at - call.started_at).total_seconds()
        
        return {
            "call_id": call.id,
            "user_id": call.user_id,
            "status": call.status,
            "started_at": call.started_at.isoformat(),
            "ended_at": call.ended_at.isoformat() if call.ended_at else None,
            "duration_seconds": duration,
            "unlimited": True
        }
    except Exception as e:
        logger.error(f"Error getting call: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{call_id}/end")
async def end_call(call_id: str, db: AsyncSession = Depends(get_db)):
    """
    End a video call session
    """
    try:
        result = await db.execute(select(Call).where(Call.id == call_id))
        call = result.scalars().first()
        
        if not call:
            raise HTTPException(status_code=404, detail="Call not found")
        
        call.status = "ended"
        call.ended_at = datetime.utcnow()
        call.duration_seconds = (call.ended_at - call.started_at).total_seconds()
        
        await db.commit()
        
        logger.info(f"Call {call_id} ended. Duration: {call.duration_seconds}s")
        
        return {
            "call_id": call_id,
            "status": "ended",
            "duration_seconds": call.duration_seconds
        }
    except Exception as e:
        logger.error(f"Error ending call: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{call_id}/sessions")
async def get_call_sessions(call_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get all sessions for a call
    """
    try:
        result = await db.execute(
            select(CallSession).where(CallSession.call_id == call_id)
        )
        sessions = result.scalars().all()
        
        return {
            "call_id": call_id,
            "session_count": len(sessions),
            "sessions": [
                {
                    "session_id": s.session_id,
                    "is_active": s.is_active,
                    "started_at": s.started_at.isoformat(),
                    "total_messages": s.total_messages
                }
                for s in sessions
            ]
        }
    except Exception as e:
        logger.error(f"Error getting sessions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
