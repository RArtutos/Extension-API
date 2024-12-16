from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..db.database import Database
from ..schemas.account import Account, AccountCreate, AccountStatus
from ..core.auth import get_current_user
from ..core.config import settings

router = APIRouter()
db = Database()

@router.get("/", response_model=List[Account])
async def get_accounts(current_user: dict = Depends(get_current_user)):
    return db.get_accounts(current_user["email"])

@router.get("/{account_id}/status", response_model=AccountStatus)
async def get_account_status(account_id: int, current_user: dict = Depends(get_current_user)):
    accounts = db.get_accounts(current_user["email"])
    account = next((a for a in accounts if a["id"] == account_id), None)
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
        
    return {
        "id": account["id"],
        "active_sessions": account["active_sessions"],
        "max_concurrent_users": account["max_concurrent_users"],
        "active_users": account["active_users"]
    }

@router.post("/session/{account_id}/start")
async def start_session(account_id: int, current_user: dict = Depends(get_current_user)):
    if not db.increment_session_count(current_user["email"], account_id):
        raise HTTPException(
            status_code=400,
            detail="Could not start session. Maximum concurrent users reached."
        )
    return {"message": "Session started successfully"}

@router.post("/session/{account_id}/end")
async def end_session(account_id: int, current_user: dict = Depends(get_current_user)):
    if not db.decrement_session_count(current_user["email"], account_id):
        raise HTTPException(
            status_code=400,
            detail="Could not end session"
        )
    return {"message": "Session ended successfully"}

@router.post("/activity/{account_id}")
async def update_activity(
    account_id: int,
    domain: str,
    current_user: dict = Depends(get_current_user)
):
    if not db.update_user_activity(current_user["email"], account_id, domain):
        raise HTTPException(
            status_code=400,
            detail="Could not update activity"
        )
    return {"message": "Activity updated successfully"}

# ... (rest of the routes remain unchanged)