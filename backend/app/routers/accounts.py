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

@router.get("/{account_id}/session", response_model=dict)
async def get_session_info(account_id: int, current_user: dict = Depends(get_current_user)):
    account = db.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    sessions = db.get_active_sessions(account_id)
    return {
        "active_sessions": len(sessions),
        "max_concurrent_users": account.get("max_concurrent_users", settings.MAX_CONCURRENT_USERS_PER_ACCOUNT)
    }

@router.post("/", response_model=Account)
async def create_account(account: AccountCreate, current_user: dict = Depends(get_current_user)):
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Not enough privileges")
        
    # Create the account
    created_account = db.create_account(account.dict())
    
    # Assign the account to the current user
    if created_account:
        db.assign_account_to_user(current_user["email"], created_account["id"])
        
    return created_account

@router.delete("/{account_id}")
async def delete_account(account_id: int, current_user: dict = Depends(get_current_user)):
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Not enough privileges")
        
    if not db.delete_account(account_id):
        raise HTTPException(status_code=404, detail="Account not found")
        
    return {"message": "Account deleted"}