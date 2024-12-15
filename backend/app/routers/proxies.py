from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..db import models
from ..schemas import proxy as proxy_schema

router = APIRouter()

@router.get("/")
def get_proxies(db: Session = Depends(get_db)):
    return db.query(models.Proxy).all()

@router.post("/")
def create_proxy(proxy: proxy_schema.ProxyCreate, db: Session = Depends(get_db)):
    db_proxy = models.Proxy(**proxy.dict())
    db.add(db_proxy)
    db.commit()
    db.refresh(db_proxy)
    return db_proxy

@router.delete("/{proxy_id}")
def delete_proxy(proxy_id: int, db: Session = Depends(get_db)):
    proxy = db.query(models.Proxy).filter(models.Proxy.id == proxy_id).first()
    if not proxy:
        raise HTTPException(status_code=404, detail="Proxy not found")
    db.delete(proxy)
    db.commit()
    return {"message": "Proxy deleted"}