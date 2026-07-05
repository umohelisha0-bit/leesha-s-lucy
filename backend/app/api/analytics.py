"""Analytics endpoints"""
import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models import Call, Message
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/calls")
async def get_call_history(user_id: str = None, limit: int = 50, db: AsyncSession = Depends(get_db)):
    """
    Get call history
    """
    try:
        query = select(Call)
        
        if user_id:
            query = query.where(Call.user_id == user_id)
        
        query = query.order_by(Call.created_at.desc()).limit(limit)
        result = await db.execute(query)
        calls = result.scalars().all()
        
        return {
            "total_calls": len(calls),
            "calls": [
                {
                    "call_id": c.id,
                    "user_id": c.user_id,
                    "status": c.status,
                    "started_at": c.started_at.isoformat(),
                    "ended_at": c.ended_at.isoformat() if c.ended_at else None,
                    "duration_seconds": c.duration_seconds
                }
                for c in calls
            ]
        }
    except Exception as e:
        logger.error(f"Error getting call history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_statistics(user_id: str = None, days: int = 30, db: AsyncSession = Depends(get_db)):
    """
    Get usage statistics
    """
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        query = select(Call).where(Call.created_at >= cutoff_date)
        
        if user_id:
            query = query.where(Call.user_id == user_id)
        
        result = await db.execute(query)
        calls = result.scalars().all()
        
        # Calculate statistics
        total_calls = len(calls)
        total_duration = sum(
            (c.duration_seconds or 0) for c in calls if c.status == "ended"
        )
        active_calls = sum(1 for c in calls if c.status == "active")
        
        # Get message count
        msg_result = await db.execute(
            select(func.count(Message.id)).where(
                Message.created_at >= cutoff_date
            )
        )
        total_messages = msg_result.scalar() or 0
        
        return {
            "period_days": days,
            "total_calls": total_calls,
            "active_calls": active_calls,
            "total_duration_seconds": total_duration,
            "average_call_duration_seconds": total_duration / total_calls if total_calls > 0 else 0,
            "total_messages": total_messages,
            "unlimited_features": {
                "no_time_limits": True,
                "no_session_timeout": True,
                "no_watermarks": True,
                "unlimited_messages": True
            }
        }
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/messages/{call_id}")
async def get_call_messages(call_id: str, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Get messages for a specific call
    """
    try:
        result = await db.execute(
            select(Message)
            .where(Message.call_id == call_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        messages = result.scalars().all()
        
        return {
            "call_id": call_id,
            "message_count": len(messages),
            "messages": [
                {
                    "id": m.id,
                    "sender": m.sender,
                    "content": m.content,
                    "type": m.message_type,
                    "created_at": m.created_at.isoformat()
                }
                for m in messages
            ]
        }
    except Exception as e:
        logger.error(f"Error getting messages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
