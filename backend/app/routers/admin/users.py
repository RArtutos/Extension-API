"""Admin users routes"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ...core.auth import get_current_admin_user
from ...db.database import Database
from ...schemas.user import UserCreate, UserResponse

router = APIRouter()
db = Database()

@router.get("/", response_model=List[UserResponse])
async def get_users(current_user: dict = Depends(get_current_admin_user)):
    """Get all users"""
    users = db.get_users()
    return users

@router.post("/create", response_model=UserResponse)
async def create_user(user: UserCreate, current_user: dict = Depends(get_current_admin_user)):
    """Create new user"""
    if db.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
        
    # Create user first
    created_user = db.create_user(user.dict())
    
    # If preset is specified, apply its accounts
    if user.preset_id:
        preset = db.get_preset(user.preset_id)
        if preset and preset.get("account_ids"):
            for account_id in preset["account_ids"]:
                db.assign_account_to_user(user.email, account_id)
                
    return created_user

@router.get("/{user_id}/accounts")
async def get_user_accounts(user_id: str, current_user: dict = Depends(get_current_admin_user)):
    """Get accounts assigned to a user"""
    user = db.get_user_by_email(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return db.get_accounts(user_id)