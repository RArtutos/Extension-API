from pydantic import BaseModel, EmailStr, conint
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    is_admin: bool = False
    expires_in_days: Optional[int] = None
    preset_id: Optional[int] = None
    max_devices: conint(ge=1) = 1  # Default to 1 device

class UserUpdate(UserBase):
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    expires_in_days: Optional[int] = None
    preset_id: Optional[int] = None
    max_devices: Optional[conint(ge=1)] = None

class UserSession(BaseModel):
    device_id: str
    last_active: datetime
    ip_address: str
    user_agent: str

class UserAnalytics(BaseModel):
    total_logins: int
    active_sessions: int
    account_usage: List[dict]  # List of accounts and usage time
    last_activities: List[dict]  # Recent activities