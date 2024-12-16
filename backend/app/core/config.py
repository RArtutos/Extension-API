import json
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from .auth import get_password_hash
from datetime import datetime

class Settings(BaseSettings):
    SECRET_KEY: str = "artutos123"
    ADMIN_EMAIL: str = "admin@artutos.eu.org"
    ADMIN_PASSWORD: str = "artutos123"
    DATA_FILE: str = "data/db.json"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    COOKIE_INACTIVITY_TIMEOUT: int = 600  # 10 minutes
    MAX_CONCURRENT_USERS_PER_ACCOUNT: int = 3

    def init_data_file(self):
        data_file = Path(self.DATA_FILE)
        data_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not data_file.exists():
            initial_data = {
                "users": [
                    {
                        "email": self.ADMIN_EMAIL,
                        "password": get_password_hash(self.ADMIN_PASSWORD),
                        "is_admin": True,
                        "created_at": datetime.utcnow().isoformat()
                    }
                ],
                "accounts": [],
                "proxies": [],
                "user_accounts": [],
                "analytics": []
            }
            with open(data_file, 'w') as f:
                json.dump(initial_data, f, indent=2)

    class Config:
        env_file = ".env"

settings = Settings()