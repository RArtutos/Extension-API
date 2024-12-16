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
    start_time = datetime.utcnow() - timedelta(hours=24)
    return db.get_analytics(start_time)

@router.post("/users/{user_id}/accounts/{account_id}")
async def assign_account_to_user(
    user_id: str,
    account_id: int,
    current_user: dict = Depends(get_current_admin_user)
):
    data = db._read_data()
    
    # Verify user exists
    user = db.get_user_by_email(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify account exists
    account = next((a for a in data["accounts"] if a["id"] == account_id), None)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Create user_account entry if it doesn't exist
    user_account = next(
        (ua for ua in data["user_accounts"] 
         if ua["user_id"] == user_id and ua["account_id"] == account_id),
        None
    )
    
    if not user_account:
        data["user_accounts"].append({
            "user_id": user_id,
            "account_id": account_id,
            "active_sessions": 0,
            "last_activity": None
        })
        db._write_data(data)
        
    return {"message": "Account assigned successfully"}

@router.delete("/users/{user_id}/accounts/{account_id}")
async def remove_account_from_user(
    user_id: str,
    account_id: int,
    current_user: dict = Depends(get_current_admin_user)
):
    data = db._read_data()
    data["user_accounts"] = [
        ua for ua in data["user_accounts"]
        if not (ua["user_id"] == user_id and ua["account_id"] == account_id)
    ]
    db._write_data(data)
    return {"message": "Account removed successfully"}