from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Cookie(BaseModel):
    domain: str
    name: str
    value: str
    path: str = "/"

class AccountBase(BaseModel):
    name: str
    group: Optional[int] = None  # Changed to int to match group_id
    cookies: List[Cookie] = Field(default_factory=list)
    max_concurrent_users: int = 1  # Default to 1

class AccountCreate(AccountBase):
    pass

class ActiveUser(BaseModel):
    user_id: str
    sessions: int
    last_activity: Optional[str]

class AccountStatus(BaseModel):
    id: int
    active_sessions: int
    max_concurrent_users: int
    active_users: List[ActiveUser]

class Account(AccountBase):
    id: int
    active_sessions: int = 0
    max_concurrent_users: int = 1  # Default to 1
    active_users: List[ActiveUser] = Field(default_factory=list)
    group: Optional[str] = None  # Group name for display