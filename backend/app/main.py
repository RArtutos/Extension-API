from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, cookies, proxies
from .core.config import settings
from .db.session import engine
from .db import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cookie Manager API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(cookies.router, prefix="/api/cookies", tags=["cookies"])
app.include_router(proxies.router, prefix="/api/proxies", tags=["proxies"])