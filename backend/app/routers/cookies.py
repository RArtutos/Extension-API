from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..db import models

router = APIRouter()

@router.get("/profile/{profile_id}")
def get_cookies(profile_id: int, db: Session = Depends(get_db)):
    cookies = db.query(models.Cookie).filter(models.Cookie.profile_id == profile_id).all()
    return cookies

@router.post("/profile/{profile_id}")
def create_cookie(profile_id: int, cookie_data: dict, db: Session = Depends(get_db)):
    cookie = models.Cookie(**cookie_data, profile_id=profile_id)
    db.add(cookie)
    db.commit()
    db.refresh(cookie)
    return cookie

@router.delete("/{cookie_id}")
def delete_cookie(cookie_id: int, db: Session = Depends(get_db)):
    cookie = db.query(models.Cookie).filter(models.Cookie.id == cookie_id).first()
    if not cookie:
        raise HTTPException(status_code=404, detail="Cookie not found")
    db.delete(cookie)
    db.commit()
    return {"message": "Cookie deleted"}