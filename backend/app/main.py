from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, accounts, proxies, analytics
from .routers.admin import router as admin_router
from .routers.admin.analytics import router as admin_analytics_router
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
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
app.include_router(admin_analytics_router, prefix="/api/admin/analytics", tags=["admin-analytics"])

@app.on_event("startup")
async def startup_event():
    settings.init_data_file()