from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..db.database import Database
from ..core.auth import get_current_admin_user
from ..schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/api/admin")
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

@router.get("/users/{user_id}/accounts")
async def get_user_accounts(user_id: str, current_user: dict = Depends(get_current_admin_user)):
    user = db.get_user_by_email(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return db.get_accounts(user_id)

@router.post("/users/{user_id}/accounts/{account_id}")
async def assign_account(
    user_id: str, 
    account_id: int, 
    current_user: dict = Depends(get_current_admin_user)
):
    if not db.assign_account_to_user(user_id, account_id):
        raise HTTPException(status_code=400, detail="Failed to assign account")
    return {"message": "Account assigned successfully"}

@router.delete("/users/{user_id}/accounts/{account_id}")
async def remove_account(
    user_id: str, 
    account_id: int, 
    current_user: dict = Depends(get_current_admin_user)
):
    if not db.remove_account_from_user(user_id, account_id):
        raise HTTPException(status_code=400, detail="Failed to remove account")
    return {"message": "Account removed successfully"}