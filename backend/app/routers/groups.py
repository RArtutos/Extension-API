from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..db.repositories.group_repository import GroupRepository
from ..schemas.group import Group, GroupCreate, GroupWithAccounts
from ..core.auth import get_current_admin_user

router = APIRouter()
group_repo = GroupRepository()

@router.get("/", response_model=List[GroupWithAccounts])
async def get_groups(current_user: dict = Depends(get_current_admin_user)):
    try:
        groups = group_repo.get_all()
        for group in groups:
            group["accounts"] = group_repo.get_accounts_by_group(group["id"])
        return groups
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=Group)
async def create_group(group: GroupCreate, current_user: dict = Depends(get_current_admin_user)):
    try:
        if not group.name:
            raise HTTPException(status_code=400, detail="Group name is required")
        
        new_group = group_repo.create(group.dict())
        if not new_group:
            raise HTTPException(status_code=400, detail="Failed to create group")
        
        return new_group
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{group_id}", response_model=GroupWithAccounts)
async def get_group(group_id: int, current_user: dict = Depends(get_current_admin_user)):
    group = group_repo.get_by_id(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    group["accounts"] = group_repo.get_accounts_by_group(group_id)
    return group

@router.post("/{group_id}/accounts/{account_id}")
async def assign_account_to_group(
    group_id: int,
    account_id: int,
    current_user: dict = Depends(get_current_admin_user)
):
    try:
        if group_repo.assign_account(group_id, account_id):
            return {"message": "Account assigned to group successfully"}
        raise HTTPException(status_code=400, detail="Failed to assign account to group")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))