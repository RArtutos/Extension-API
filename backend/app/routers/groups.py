from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas.group import Group, GroupCreate
from ..core.auth import get_current_admin_user
from ..db.database import Database

router = APIRouter()
db = Database()

@router.get("/", response_model=List[Group])
async def get_groups(current_user: dict = Depends(get_current_admin_user)):
    return db.get_groups()

@router.post("/", response_model=Group)
async def create_group(
    group: GroupCreate,
    current_user: dict = Depends(get_current_admin_user)
):
    if not group.name:
        raise HTTPException(status_code=400, detail="Group name is required")
    
    new_group = db.create_group(group.dict())
    if not new_group:
        raise HTTPException(status_code=400, detail="Failed to create group")
    
    return new_group

@router.post("/{group_id}/accounts/{account_id}")
async def assign_account_to_group(
    group_id: int,
    account_id: int,
    current_user: dict = Depends(get_current_admin_user)
):
    if not db.assign_group_to_account(account_id, group_id):
        raise HTTPException(status_code=400, detail="Failed to assign account to group")
    return {"message": "Account assigned to group successfully"}