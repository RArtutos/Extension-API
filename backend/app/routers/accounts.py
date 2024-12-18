from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict
from ..db.database import Database
from ..schemas.account import Account, AccountCreate
from ..core.auth import get_current_user
from ..core.session_manager import SessionManager

router = APIRouter()
db = Database()
session_manager = SessionManager()

@router.get("/", response_model=List[Account])
async def get_accounts(current_user: dict = Depends(get_current_user)):
    return db.get_accounts(current_user["email"])

@router.get("/{account_id}", response_model=Account)
async def get_account(account_id: int, current_user: dict = Depends(get_current_user)):
    account = db.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.get("/{account_id}/session", response_model=dict)
async def get_session_info(account_id: int, current_user: dict = Depends(get_current_user)):
    """Get session information for an account"""
    return session_manager.get_session_info(account_id)

@router.put("/{account_id}/session")
async def update_session(
    account_id: int,
    session_data: Dict,
    current_user: dict = Depends(get_current_user)
):
    """Update session status for an account"""
    # Add user_id to session data
    session_data['user_id'] = current_user['email']
    
    if not session_manager.update_session(account_id, session_data):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update session. Maximum concurrent users reached."
        )
    return {"success": True}

@router.post("/{account_id}/session/start")
async def start_session(
    account_id: int,
    domain: str,
    current_user: dict = Depends(get_current_user)
):
    """Start a new session"""
    if not session_manager.start_session(account_id, current_user['email'], domain):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to start session. Maximum concurrent users reached."
        )
    return {"success": True}

@router.post("/{account_id}/session/end")
async def end_session(
    account_id: int,
    current_user: dict = Depends(get_current_user)
):
    """End a session"""
    if not session_manager.end_session(account_id, current_user['email']):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to end session"
        )
    return {"success": True}