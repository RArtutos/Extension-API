from fastapi import APIRouter
from .users import router as users_router
from .analytics import router as analytics_router

router = APIRouter(prefix="/admin", tags=["admin"])

# Include sub-routers
router.include_router(users_router)
router.include_router(analytics_router)