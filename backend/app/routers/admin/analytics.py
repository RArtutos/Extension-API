from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from ...core.auth import get_current_admin_user
from ...core.analytics_manager import AnalyticsManager

router = APIRouter()
analytics_manager = AnalyticsManager()

@router.get("/analytics")
async def get_analytics_dashboard(current_user: dict = Depends(get_current_admin_user)):
    """Get general analytics dashboard"""
    return analytics_manager.get_dashboard_data()