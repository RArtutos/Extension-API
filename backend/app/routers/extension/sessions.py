from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from ...core.auth import get_current_user
from ...db.database import Database
from ...schemas.extension import SessionCreate, SessionUpdate, SessionResponse

router = APIRouter(prefix="/sessions", tags=["extension-sessions"])
db = Database()

@router.post("/{account_id}/start", response_model=SessionResponse)
async def start_session(
    account_id: int,
    session_data: SessionCreate,
    current_user: Dict = Depends(get_current_user)
):
    """Start a new session for an account"""
    try:
        # Verify session limits
        session_info = db.get_session_info(account_id)
        if session_info["active_sessions"] >= session_info["max_concurrent_users"]:
            raise HTTPException(
                status_code=400,
                detail="Maximum concurrent users reached"
            )

        # Create session
        session = db.create_session({
            "user_id": current_user["email"],
            "account_id": account_id,
            "device_id": session_data.device_id,
            "domain": session_data.domain,
            "ip_address": session_data.ip_address,
            "user_agent": session_data.user_agent
        })
        
        return {
            "session_id": session["id"],
            "status": "active",
            "created_at": session["created_at"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{account_id}/update", response_model=SessionResponse)
async def update_session(
    account_id: int,
    session_data: SessionUpdate,
    current_user: Dict = Depends(get_current_user)
):
    """Update an existing session"""
    try:
        session = db.update_session_activity(
            current_user["email"],
            account_id,
            session_data.domain
        )
        
        return {
            "session_id": session["id"],
            "status": "active",
            "last_activity": session["last_activity"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{account_id}/end")
async def end_session(
    account_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """End a session"""
    try:
        db.end_session(current_user["email"], account_id)
        return {"status": "success", "message": "Session ended successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))