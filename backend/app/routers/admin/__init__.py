from fastapi import APIRouter
from . import users, presets

router = APIRouter(prefix="/admin")
router.include_router(users.router)
router.include_router(presets.router)