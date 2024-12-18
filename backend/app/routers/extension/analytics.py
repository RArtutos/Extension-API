from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List
from ...core.auth import get_current_user
from ...db.database import Database
from ...schemas.extension import AnalyticsEvent, BatchAnalyticsEvents

router = APIRouter(prefix="/analytics", tags=["extension-analytics"])
db = Database()

@router.post("/events")
async def track_event(
    event: AnalyticsEvent,
    current_user: Dict = Depends(get_current_user)
):
    """Track a single analytics event"""
    try:
        db.create_analytics_event({
            "user_id": current_user["email"],
            "account_id": event.account_id,
            "domain": event.domain,
            "action": event.action,
            "timestamp": event.timestamp,
            "metadata": event.metadata
        })
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/events/batch")
async def track_events_batch(
    events: BatchAnalyticsEvents,
    current_user: Dict = Depends(get_current_user)
):
    """Track multiple analytics events in batch"""
    try:
        for event in events.events:
            db.create_analytics_event({
                "user_id": current_user["email"],
                "account_id": event.account_id,
                "domain": event.domain,
                "action": event.action,
                "timestamp": event.timestamp,
                "metadata": event.metadata
            })
        return {
            "status": "success",
            "processed_events": len(events.events)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))