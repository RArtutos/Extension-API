from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime, timedelta
from ..db.database import Database
from ..core.auth import get_current_admin_user
from ..schemas.user import UserCreate, UserResponse
from ..schemas.analytics import AnalyticsResponse
from ..db.repositories.group_repository import GroupRepository
from ..db.repositories.account_repository import AccountRepository

router = APIRouter()
db = Database()
group_repo = GroupRepository()
account_repo = AccountRepository()

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

@router.get("/users/{user_id}/accounts")
async def get_user_accounts(user_id: str, current_user: dict = Depends(get_current_admin_user)):
    user = db.get_user_by_email(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return db.get_user_accounts(user_id)

@router.post("/users/{user_id}/accounts/{account_id}")
async def assign_account_to_user(
    user_id: str,
    account_id: int,
    current_user: dict = Depends(get_current_admin_user)
):
    if not db.assign_account_to_user(user_id, account_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to assign account"
        )
    return {"message": "Account assigned successfully"}

@router.post("/users/{user_id}/groups/{group_id}")
async def assign_group_to_user(
    user_id: str,
    group_id: int,
    current_user: dict = Depends(get_current_admin_user)
):
    try:
        # Get all accounts in the group
        group = group_repo.get_by_id(group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
            
        accounts = group_repo.get_accounts_by_group(group_id)
        success = True
        
        # Assign each account to the user
        for account in accounts:
            if not db.assign_account_to_user(user_id, account["id"]):
                success = False
                
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Some accounts could not be assigned"
            )
            
        return {"message": "Group accounts assigned successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/users/{user_id}/accounts/{account_id}")
async def remove_account_from_user(
    user_id: str,
    account_id: int,
    current_user: dict = Depends(get_current_admin_user)
):
    if not db.remove_account_from_user(user_id, account_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to remove account"
        )
    return {"message": "Account removed successfully"}

@router.get("/analytics")
async def get_analytics(current_user: dict = Depends(get_current_admin_user)):
    start_time = datetime.utcnow() - timedelta(hours=24)
    return db.get_analytics(start_time)