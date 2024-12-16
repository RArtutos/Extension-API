from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..db.database import Database
from ..core.auth import get_current_admin_user
from ..schemas.user import UserCreate, UserResponse
from ..schemas.preset import PresetCreate, PresetUpdate, Preset

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
    return db.create_user(
        user.email, 
        user.password, 
        user.is_admin,
        expires_in_days=user.expires_in_days,
        preset_id=user.preset_id
    )

@router.get("/presets", response_model=List[Preset])
async def get_presets(current_user: dict = Depends(get_current_admin_user)):
    return db.get_presets()

@router.post("/presets", response_model=Preset)
async def create_preset(preset: PresetCreate, current_user: dict = Depends(get_current_admin_user)):
    return db.create_preset(preset.dict())

@router.put("/presets/{preset_id}", response_model=Preset)
async def update_preset(
    preset_id: int, 
    preset: PresetUpdate, 
    current_user: dict = Depends(get_current_admin_user)
):
    updated_preset = db.update_preset(preset_id, preset.dict())
    if not updated_preset:
        raise HTTPException(status_code=404, detail="Preset not found")
    return updated_preset

@router.delete("/presets/{preset_id}")
async def delete_preset(preset_id: int, current_user: dict = Depends(get_current_admin_user)):
    if not db.delete_preset(preset_id):
        raise HTTPException(status_code=404, detail="Preset not found")
    return {"message": "Preset deleted successfully"}