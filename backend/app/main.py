from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, accounts, proxies
from .core.config import settings

app = FastAPI(title="Account Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with correct prefixes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])
app.include_router(proxies.router, prefix="/api/proxies", tags=["proxies"])

# Include admin routers
from .routers.admin.users import router as users_router
from .routers.admin.presets import router as presets_router

app.include_router(users_router, prefix="/api/admin/users", tags=["users"])
app.include_router(presets_router, prefix="/api/admin/presets", tags=["presets"])

@app.on_event("startup")
async def startup_event():
    settings.init_data_file()