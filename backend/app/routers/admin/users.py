from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ...db.database import Database
from ...core.auth import get_current_admin_user
from ...schemas.user import UserCreate, UserResponse

router = APIRouter()
db = Database()

@router.get("/", response_model=List[UserResponse])
async def get_users(current_user: dict = Depends(get_current_admin_user)):
    users = db.get_users()
    # Ensure max_devices is set for each user
    for user in users:
        if 'max_devices' not in user:
            user['max_devices'] = 1
    return users

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, current_user: dict = Depends(get_current_admin_user)):
    if db.get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return db.create_user(user.dict())