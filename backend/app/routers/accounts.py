from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..db.database import Database
from ..schemas.account import Account, AccountCreate
from .auth import oauth2_scheme

router = APIRouter()
db = Database()

@router.get("/", response_model=List[Account])
async def get_accounts(token: str = Depends(oauth2_scheme)):
    return db.get_accounts()

@router.post("/", response_model=Account)
async def create_account(account: AccountCreate, token: str = Depends(oauth2_scheme)):
    # Validate cookies format
    for cookie in account.cookies:
        if not cookie.domain or not cookie.name or not cookie.value:
            raise HTTPException(
                status_code=400,
                detail="Invalid cookie format. Required fields: domain, name, value"
            )
    
    return db.create_account(account.dict())

@router.delete("/{account_id}")
async def delete_account(account_id: int, token: str = Depends(oauth2_scheme)):
    if not db.delete_account(account_id):
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account deleted"}