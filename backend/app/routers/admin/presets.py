from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ...core.auth import get_current_admin_user
from ...core.preset_manager import PresetManager
from ...schemas.preset import PresetCreate, PresetUpdate, Preset

router = APIRouter(prefix="/presets", tags=["presets"])
preset_manager = PresetManager()

@router.get("/", response_model=List[Preset])
async def get_presets(current_user: dict = Depends(get_current_admin_user)):
    return preset_manager.get_all_presets()

@router.post("/", response_model=Preset)
async def create_preset(preset: PresetCreate, current_user: dict = Depends(get_current_admin_user)):
    return preset_manager.create_preset(preset.dict())

@router.get("/{preset_id}", response_model=Preset)
async def get_preset(preset_id: int, current_user: dict = Depends(get_current_admin_user)):
    preset = preset_manager.get_preset(preset_id)
    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")
    return preset

@router.put("/{preset_id}", response_model=Preset)
async def update_preset(
    preset_id: int,
    preset: PresetUpdate,
    current_user: dict = Depends(get_current_admin_user)
):
    updated_preset = preset_manager.update_preset(preset_id, preset.dict())
    if not updated_preset:
        raise HTTPException(status_code=404, detail="Preset not found")
    return updated_preset

@router.delete("/{preset_id}")
async def delete_preset(preset_id: int, current_user: dict = Depends(get_current_admin_user)):
    if not preset_manager.delete_preset(preset_id):
        raise HTTPException(status_code=404, detail="Preset not found")
    return {"message": "Preset deleted successfully"}