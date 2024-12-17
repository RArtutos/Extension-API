from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ...db.database import Database
from ...core.auth import get_current_admin_user
from ...schemas.user import UserCreate, UserResponse

router = APIRouter()
db = Database()

@router.get("/", response_model=List[UserResponse])
async def get_users(current_user: dict = Depends(get_current_admin_user)):
    return db.get_users()

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, current_user: dict = Depends(get_current_admin_user)):
    if db.get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return db.create_user(
        user.email, 
        user.password, 
        user.is_admin,
        expires_in_days=user.expires_in_days,
        preset_id=user.preset_id
    )

@router.get("/{user_id}/accounts")
async def get_user_accounts(user_id: str, current_user: dict = Depends(get_current_admin_user)):
    user = db.get_user_by_email(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return db.get_accounts(user_id)

@router.delete("/{user_id}")
async def delete_user(user_id: str, current_user: dict = Depends(get_current_admin_user)):
    if current_user["email"] == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    user = db.get_user_by_email(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete admin users"
        )
        
    return {"message": "User deleted successfully"}