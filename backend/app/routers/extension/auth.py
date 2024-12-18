from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict
from ...core.auth import verify_password, create_access_token
from ...db.database import Database
from ...schemas.auth import TokenResponse, UserInfo

router = APIRouter(prefix="/auth", tags=["extension-auth"])
db = Database()

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm):
    """Login endpoint optimized for extension"""
    user = db.get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    token_data = {
        "sub": user["email"],
        "is_admin": user.get("is_admin", False),
        "max_devices": user.get("max_devices", 1)
    }
    
    access_token = create_access_token(token_data)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": {
            "email": user["email"],
            "is_admin": user.get("is_admin", False),
            "max_devices": user.get("max_devices", 1)
        }
    }

@router.get("/validate", response_model=UserInfo)
async def validate_token(current_user: Dict = Depends(get_current_user)):
    """Validate token and return user info"""
    return {
        "email": current_user["email"],
        "is_admin": current_user.get("is_admin", False),
        "max_devices": current_user.get("max_devices", 1)
    }