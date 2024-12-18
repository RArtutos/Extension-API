from fastapi import APIRouter
from .auth import router as auth_router
from .accounts import router as accounts_router
from .sessions import router as sessions_router
from .analytics import router as analytics_router

router = APIRouter(prefix="/api/ext", tags=["extension"])

router.include_router(auth_router)
router.include_router(accounts_router)
router.include_router(sessions_router)
router.include_router(analytics_router)