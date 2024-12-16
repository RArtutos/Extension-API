from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..db.repositories.account_repository import AccountRepository
from ..schemas.account import Account, AccountCreate, AccountStatus
from ..core.auth import get_current_user
from ..core.config import settings

router = APIRouter()
account_repository = AccountRepository()

@router.get("/", response_model=List[Account])
async def get_accounts(current_user: dict = Depends(get_current_user)):
    return account_repository.get_all(current_user["email"])

@router.post("/", response_model=Account)
async def create_account(account: AccountCreate, current_user: dict = Depends(get_current_user)):
    try:
        if not account.name:
            raise HTTPException(status_code=400, detail="Account name is required")
        new_account = account_repository.create(account.dict())
        if not new_account:
            raise HTTPException(status_code=400, detail="Failed to create account")
        return new_account
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{account_id}/status", response_model=AccountStatus)
async def get_account_status(account_id: int, current_user: dict = Depends(get_current_user)):
    account = account_repository.get_by_id(account_id)
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
    if not account_repository.increment_session_count(current_user["email"], account_id):
        raise HTTPException(
            status_code=400,
            detail="Could not start session. Maximum concurrent users reached."
        )
    return {"message": "Session started successfully"}

@router.post("/session/{account_id}/end")
async def end_session(account_id: int, current_user: dict = Depends(get_current_user)):
    if not account_repository.decrement_session_count(current_user["email"], account_id):
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
    if not account_repository.update_user_activity(current_user["email"], account_id, domain):
        raise HTTPException(
            status_code=400,
            detail="Could not update activity"
        )
    return {"message": "Activity updated successfully"}