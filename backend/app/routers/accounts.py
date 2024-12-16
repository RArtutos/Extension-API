from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..db.repositories.account_repository import AccountRepository
from ..schemas.account import Account, AccountCreate, AccountStatus
from ..core.auth import get_current_user
from ..core.config import settings

router = APIRouter()
account_repository = AccountRepository()

@router.get("/", response_model=List[Account])
async def get_accounts(current_user: dict = Depends(get_current_user)):
    """Get all accounts for the current user"""
    try:
        return account_repository.get_all(current_user["email"])
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving accounts: {str(e)}"
        )

@router.post("/", response_model=Account)
async def create_account(account: AccountCreate, current_user: dict = Depends(get_current_user)):
    """Create a new account"""
    try:
        if not account.name:
            raise HTTPException(status_code=400, detail="Account name is required")

        account_data = account.dict()
        new_account = account_repository.create(account_data)
        
        if not new_account:
            raise HTTPException(
                status_code=400, 
                detail="Failed to create account. Please check the provided data."
            )
            
        return new_account
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating the account: {str(e)}"
        )

@router.get("/{account_id}/status", response_model=AccountStatus)
async def get_account_status(account_id: int, current_user: dict = Depends(get_current_user)):
    """Get the current status of an account including active sessions"""
    status = account_repository.get_status(account_id)
    if not status:
        raise HTTPException(status_code=404, detail="Account not found")
    return status