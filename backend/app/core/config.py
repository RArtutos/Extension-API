import json
import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "artutos123"
    ADMIN_EMAIL: str = "admin@artutos.eu.org"
    ADMIN_PASSWORD: str = "artutos123"
    DATA_FILE: str = "data/db.json"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    def init_data_file(self):
        data_file = Path(self.DATA_FILE)
        data_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not data_file.exists():
            initial_data = {
                "users": [
                    {
                        "email": self.ADMIN_EMAIL,
                        "password": self.ADMIN_PASSWORD,
                        "is_admin": True
                    }
                ],
                "accounts": [],
                "proxies": []
            }
            with open(data_file, 'w') as f:
                json.dump(initial_data, f, indent=2)

    class Config:
        env_file = ".env"

settings = Settings()