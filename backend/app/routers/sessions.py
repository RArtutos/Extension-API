from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from ..core.auth import get_current_user
from ..db.database import Database
from datetime import datetime

router = APIRouter()
db = Database()

@router.post("/api/sessions")
async def create_session(
    session_data: Dict,
    current_user: dict = Depends(get_current_user)
):
    """Create a new session"""
    try:
        session_data.update({
            "user_id": current_user["email"],
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "active": True
        })
        
        if db.create_session(session_data):
            return {"success": True, "message": "Session created successfully"}
        raise HTTPException(status_code=400, detail="Failed to create session")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/sessions/{account_id}")
async def update_session(
    account_id: int,
    session_data: Dict,
    current_user: dict = Depends(get_current_user)
):
    """Update session activity"""
    try:
        success = db.update_session_activity(
            current_user["email"],
            account_id,
            session_data.get("domain")
        )
        if success:
            return {"success": True, "message": "Session updated successfully"}
        raise HTTPException(status_code=400, detail="Failed to update session")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/sessions/{account_id}")
async def end_session(
    account_id: int,
    current_user: dict = Depends(get_current_user)
):
    """End a session"""
    try:
        if db.end_session(current_user["email"], account_id):
            return {"success": True, "message": "Session ended successfully"}
        raise HTTPException(status_code=400, detail="Failed to end session")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))