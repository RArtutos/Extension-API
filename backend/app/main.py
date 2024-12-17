from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, accounts, proxies, analytics
from .routers.admin import users, analytics as admin_analytics
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
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(users.router, prefix="/api/admin/users", tags=["admin-users"])
app.include_router(admin_analytics.router, prefix="/api/admin/analytics", tags=["admin-analytics"])

@app.on_event("startup")
async def startup_event():
    settings.init_data_file()