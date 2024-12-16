from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    is_admin: bool = False
    expires_in_days: Optional[int] = None
    preset_id: Optional[int] = None

class UserUpdate(UserBase):
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    expires_in_days: Optional[int] = None
    preset_id: Optional[int] = None

class UserResponse(UserBase):
    is_admin: bool
    created_at: datetime
    expires_at: Optional[datetime] = None
    preset_id: Optional[int] = None
    preset_name: Optional[str] = None
    is_active: bool
    assigned_accounts: List[int] = []

    class Config:
        from_attributes = True