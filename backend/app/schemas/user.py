from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    is_admin: bool = False
    valid_until: Optional[datetime] = None

class UserUpdate(UserBase):
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    valid_until: Optional[datetime] = None

class UserResponse(UserBase):
    is_admin: bool
    created_at: str
    valid_until: Optional[str] = None
    assigned_accounts: List[int] = []
    active_sessions: Dict[str, str] = {}  # domain -> last_activity_timestamp
    is_expired: bool = False