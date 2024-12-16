from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..core.auth import get_current_admin_user
from ..db.database import Database
from ..schemas.user import UserCreate, UserResponse, UserAccountAssignment
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
    return db.create_user(user.email, user.password)

@router.post("/users/{user_email}/accounts/{account_id}")
async def assign_account_to_user(
    user_email: str,
    account_id: int,
    current_user: dict = Depends(get_current_admin_user)
):
    user = db.get_user_by_email(user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db.assign_account_to_user(user_email, account_id)

@router.delete("/users/{user_email}/accounts/{account_id}")
async def remove_account_from_user(
    user_email: str,
    account_id: int,
    current_user: dict = Depends(get_current_admin_user)
):
    if db.remove_account_from_user(user_email, account_id):
        return {"message": "Account removed from user"}
    raise HTTPException(status_code=404, detail="Assignment not found")

@router.get("/analytics", response_model=List[AnalyticsResponse])
async def get_analytics(
    days: int = 30,
    user_email: str = None,
    account_id: int = None,
    current_user: dict = Depends(get_current_admin_user)
):
    return db.get_analytics(days, user_email, account_id)