from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, accounts, proxies, analytics, sessions
from .routers.admin import users, analytics as admin_analytics, presets, accounts as admin_accounts
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
app.include_router(auth.router)  # This router already has the /api/auth prefix
app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])
app.include_router(proxies.router, prefix="/api/proxies", tags=["proxies"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])

# Admin routes
admin_prefix = "/api/admin"
app.include_router(users.router, prefix=f"{admin_prefix}/users", tags=["admin-users"])
app.include_router(admin_analytics.router, prefix=f"{admin_prefix}/analytics", tags=["admin-analytics"])
app.include_router(presets.router, prefix=f"{admin_prefix}/presets", tags=["admin-presets"])
app.include_router(admin_accounts.router, prefix=f"{admin_prefix}/accounts", tags=["admin-accounts"])

@app.on_event("startup")
async def startup_event():
    settings.init_data_file()

# Add root endpoint
@app.get("/")
async def root():
    return {"message": "Account Manager API"}