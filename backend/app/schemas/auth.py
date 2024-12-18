from pydantic import BaseModel, EmailStr
from typing import Optional

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_info: Optional['UserInfo'] = None

class UserInfo(BaseModel):
    email: EmailStr
    is_admin: bool = False
    max_devices: int = 1

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    is_admin: bool = False