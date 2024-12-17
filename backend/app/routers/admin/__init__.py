from fastapi import APIRouter
from .users import router as users_router
from .analytics import router as analytics_router
from .presets import router as presets_router

router = APIRouter()

# Include sub-routers
router.include_router(users_router)
router.include_router(analytics_router)
router.include_router(presets_router)