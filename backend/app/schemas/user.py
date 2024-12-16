from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    is_admin: bool = False

class UserUpdate(UserBase):
    password: Optional[str] = None
    is_admin: Optional[bool] = None

class UserResponse(UserBase):
    is_admin: bool
    created_at: str
    assigned_accounts: List[int] = []

class UserAccountAssignment(BaseModel):
    user_id: str
    account_id: int
    max_concurrent_users: int = 1
    active_sessions: int = 0
    last_activity: Optional[str] = None