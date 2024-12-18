from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..db.database import Database
from ..schemas.account import Account, AccountCreate
from ..core.auth import get_current_user
from ..core.config import settings

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
    account = db.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    active_sessions = db.get_active_sessions(account_id)
    max_users = account.get("max_concurrent_users", 1)
    
    return {
        "active_sessions": len(active_sessions),
        "max_concurrent_users": max_users
    }

@router.put("/{account_id}/session")
async def update_session(
    account_id: int, 
    session_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Update session status for an account"""
    account = db.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Validate user has access to this account
    user_accounts = db.get_user_accounts(current_user["email"])
    if account_id not in user_accounts:
        raise HTTPException(status_code=403, detail="Not authorized to access this account")
    
    try:
        # Update session data
        session_updated = db.update_session_activity(
            user_id=current_user["email"],
            account_id=account_id,
            domain=session_data.get("domain"),
            active=session_data.get("active", True)
        )
        
        if session_updated:
            return {"success": True, "message": "Session updated successfully"}
        return {"success": False, "message": "Failed to update session"}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error updating session: {str(e)}"
        )


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