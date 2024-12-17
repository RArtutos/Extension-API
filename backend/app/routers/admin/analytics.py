from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ...core.auth import get_current_user
from ...schemas.analytics import UserAnalytics, AccountAnalytics
from ...core.analytics_manager import AnalyticsManager

router = APIRouter()
analytics_manager = AnalyticsManager()

@router.get("/analytics")
async def get_analytics_dashboard(current_user: dict = Depends(get_current_user)):
    """Get general analytics dashboard"""
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return analytics_manager.get_dashboard_data()

@router.get("/analytics/user/{user_id}", response_model=UserAnalytics)
async def get_user_analytics(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get user analytics"""
    if not current_user["is_admin"] and current_user["email"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return analytics_manager.get_user_analytics(user_id)

@router.get("/analytics/account/{account_id}", response_model=AccountAnalytics)
async def get_account_analytics(
    account_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get account analytics"""
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return analytics_manager.get_account_analytics(account_id)