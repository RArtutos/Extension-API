from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..core.auth import get_current_admin_user
from ..db.database import Database
from ..schemas.user import UserCreate, UserResponse, UserAccountAssignment
from ..schemas.analytics import AnalyticsResponse
from datetime import datetime

router = APIRouter()
db = Database()

@router.get("/users", response_model=List[UserResponse])
async def get_users(current_user: dict = Depends(get_current_admin_user)):
    users = db.get_users()
    # Ensure all users have the required fields
    for user in users:
        if "created_at" not in user:
            user["created_at"] = datetime.utcnow().isoformat()
    return users

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, current_user: dict = Depends(get_current_admin_user)):
    if db.get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return db.create_user(user.email, user.password, user.is_admin)