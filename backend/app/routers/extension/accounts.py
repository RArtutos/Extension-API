from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from ...core.auth import get_current_user
from ...db.database import Database
from ...schemas.extension import ExtendedAccount, AccountSession

router = APIRouter(prefix="/accounts", tags=["extension-accounts"])
db = Database()

@router.get("/", response_model=List[ExtendedAccount])
async def get_user_accounts(current_user: Dict = Depends(get_current_user)):
    """Get all accounts available for the user with session information"""
    try:
        accounts = db.get_accounts(current_user["email"])
        result = []
        
        for account in accounts:
            session_info = db.get_session_info(account["id"])
            result.append({
                **account,
                "active_sessions": session_info.get("active_sessions", 0),
                "max_concurrent_users": session_info.get("max_concurrent_users", 1),
                "is_available": session_info.get("active_sessions", 0) < session_info.get("max_concurrent_users", 1)
            })
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{account_id}/session", response_model=AccountSession)
async def get_account_session(
    account_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """Get detailed session information for an account"""
    try:
        session_info = db.get_session_info(account_id)
        user_session = db.get_user_active_session(current_user["email"], account_id)
        
        return {
            "account_id": account_id,
            "active_sessions": session_info.get("active_sessions", 0),
            "max_concurrent_users": session_info.get("max_concurrent_users", 1),
            "current_user_session": user_session,
            "is_available": session_info.get("active_sessions", 0) < session_info.get("max_concurrent_users", 1)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))