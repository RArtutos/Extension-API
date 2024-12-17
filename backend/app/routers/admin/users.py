from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ...core.auth import get_current_admin_user
from ...db.database import Database
from ...schemas.user import UserCreate, UserResponse

router = APIRouter()
db = Database()

@router.get("/", response_model=List[UserResponse])
async def get_users(current_user: dict = Depends(get_current_admin_user)):
    users = db.get_users()
    return users

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, current_user: dict = Depends(get_current_admin_user)):
    if db.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return db.create_user(user.dict())

@router.get("/{user_id}/accounts")
async def get_user_accounts(user_id: str, current_user: dict = Depends(get_current_admin_user)):
    """Get accounts assigned to a user"""
    user = db.get_user_by_email(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return db.get_accounts(user_id)

@router.post("/{user_id}/accounts/{account_id}")
async def assign_account(
    user_id: str, 
    account_id: int, 
    current_user: dict = Depends(get_current_admin_user)
):
    """Assign account to user"""
    if not db.assign_account_to_user(user_id, account_id):
        raise HTTPException(status_code=400, detail="Failed to assign account")
    return {"message": "Account assigned successfully"}