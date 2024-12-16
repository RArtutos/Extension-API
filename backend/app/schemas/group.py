from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .account import Account

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    created_at: datetime

class GroupWithAccounts(Group):
    accounts: List[Account] = []