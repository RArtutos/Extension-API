from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime, timedelta
from ..db.database import Database
from ..core.auth import get_current_admin_user
from ..schemas.user import UserCreate, UserResponse
from ..schemas.analytics import AnalyticsResponse

router = APIRouter()
db = Database()

@router.get("/users", response_model=List[UserResponse])
async def get_users(current_user: dict = Depends(get_current_admin_user)):
    return db.get_users()

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, current_user: dict = Depends(get_current_admin_user)):
    if db.get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return db.create_user(user.email, user.password, user.is_admin)

@router.get("/analytics")
async def get_analytics(current_user: dict = Depends(get_current_admin_user)):
    # Get analytics for the last 24 hours
    start_time = datetime.utcnow() - timedelta(hours=24)
    analytics = db.get_analytics(start_time)
    
    # Get all accounts with their current status
    accounts = db.get_accounts()
    
    # Calculate hourly activity
    hourly_activity = db.get_hourly_activity(start_time)
    
    return {
        "total_sessions": analytics["total_sessions"],
        "active_accounts": analytics["active_accounts"],
        "active_users": analytics["active_users"],
        "accounts": accounts,
        "recent_activity": analytics["recent_activity"],
        "hourly_activity": hourly_activity
    }

@router.get("/groups")
async def get_groups(current_user: dict = Depends(get_current_admin_user)):
    return db.get_groups()

@router.post("/groups")
async def create_group(
    group_data: dict,
    current_user: dict = Depends(get_current_admin_user)
):
    return db.create_group(group_data)

@router.post("/accounts/{account_id}/group/{group_id}")
async def assign_group(
    account_id: int,
    group_id: int,
    current_user: dict = Depends(get_current_admin_user)
):
    if not db.assign_group_to_account(account_id, group_id):
        raise HTTPException(
            status_code=400,
            detail="Failed to assign group to account"
        )
    return {"message": "Group assigned successfully"}