from pydantic import BaseModel
from typing import List, Optional

class Cookie(BaseModel):
    domain: str
    name: str
    value: str
    path: str = "/"

class AccountBase(BaseModel):
    name: str
    group: Optional[str] = None
    cookies: List[Cookie] = []

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int