from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    is_admin: bool = False
    valid_days: Optional[int] = 30

class UserUpdate(UserBase):
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    expires_at: Optional[datetime] = None

class UserResponse(UserBase):
    is_admin: bool
    created_at: str
    expires_at: Optional[str] = None
    assigned_accounts: List[int] = []