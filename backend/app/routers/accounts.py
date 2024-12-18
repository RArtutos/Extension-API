from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..db.database import Database
from ..schemas.account import Account, AccountCreate
from ..core.auth import get_current_user
from ..core.config import settings
from typing import List, Dict
from ..core.session_manager import SessionManager


router = APIRouter()
db = Database()

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
    if not session_manager.update_session(account_id, session_data):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update session"
        )
    return {"success": True}

@router.post("/", response_model=Account)
async def create_account(account: AccountCreate, current_user: dict = Depends(get_current_user)):
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Not enough privileges")
        
    created_account = db.create_account(account.dict())
    if created_account:
        db.assign_account_to_user(current_user["email"], created_account["id"])
    return created_account

@router.put("/{account_id}", response_model=Account)
async def update_account(account_id: int, account: AccountCreate, current_user: dict = Depends(get_current_user)):
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Not enough privileges")
        
    updated_account = db.update_account(account_id, account.dict())
    if not updated_account:
        raise HTTPException(status_code=404, detail="Account not found")
    return updated_account
