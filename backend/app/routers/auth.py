from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..core.auth import verify_password, create_access_token, get_password_hash
from ..core.config import settings
from ..db.database import Database

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
db = Database()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": user["email"], "is_admin": user.get("is_admin", False)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    if not db.get_user_by_email(settings.ADMIN_EMAIL):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create new users"
        )
    
    if db.get_user_by_email(form_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(form_data.password)
    user = db.create_user(form_data.username, hashed_password)
    
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}