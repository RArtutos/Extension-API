from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from ..core.auth import get_current_user
from ..core.analytics_manager import AnalyticsManager

router = APIRouter()
analytics_manager = AnalyticsManager()

@router.get("/user/{user_id}")
async def get_user_analytics(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get analytics for a specific user"""
    if not current_user["is_admin"] and current_user["email"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return analytics_manager.get_user_analytics(user_id)

@router.get("/account/{account_id}")
async def get_account_analytics(
    account_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get analytics for a specific account"""
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return analytics_manager.get_account_analytics(account_id)

@router.post("/events/batch")
async def process_events_batch(events_data: dict):
    """Process a batch of analytics events"""
    user_id = events_data.get('user_id')
    events = events_data.get('events', [])
    
    for event in events:
        if event['type'] == 'pageview':
            await analytics_manager.track_page_view(user_id, event['domain'])
        elif event['type'] == 'account_switch':
            await analytics_manager.track_account_switch(user_id, event['from'], event['to'])
        elif event['type'] == 'session':
            if event['action'] == 'start':
                await analytics_manager.track_session_start(user_id, event['account_id'], event['domain'])
            elif event['action'] == 'end':
                await analytics_manager.track_session_end(user_id, event['account_id'], event['domain'])
    
    return {"success": True, "processed_events": len(events)}