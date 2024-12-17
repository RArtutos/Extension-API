from datetime import datetime, timedelta
from typing import Optional, List, Dict
from ..base import BaseRepository
from ...core.config import settings
from ...core.auth import get_password_hash

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(settings.DATA_FILE)

    def get_all(self) -> List[Dict]:
        data = self._read_data()
        users = data.get("users", [])
        
        for user in users:
            # Convert string timestamps to datetime objects
            if isinstance(user.get("created_at"), str):
                user["created_at"] = datetime.fromisoformat(user["created_at"])
            if user.get("expires_at") and isinstance(user["expires_at"], str):
                user["expires_at"] = datetime.fromisoformat(user["expires_at"])
            
            # Add required fields
            user["is_active"] = True
            if user.get("expires_at"):
                user["is_active"] = datetime.utcnow() < user["expires_at"]
            
            user["max_devices"] = user.get("max_devices", 1)
            user["active_sessions"] = 0
            user["assigned_accounts"] = [
                ua["account_id"] for ua in data.get("user_accounts", [])
                if ua["user_id"] == user["email"]
            ]
        
        return users

    def create(self, user_data: Dict) -> Optional[Dict]:
        data = self._read_data()
        if "users" not in data:
            data["users"] = []

        # Process expiration
        expires_in_days = user_data.pop("expires_in_days", None)
        if expires_in_days:
            user_data["expires_at"] = (datetime.utcnow() + timedelta(days=expires_in_days)).isoformat()
        else:
            user_data["expires_at"] = None

        # Set default values
        user_data["max_devices"] = user_data.get("max_devices", 1)
        user_data["active_sessions"] = 0
        user_data["created_at"] = datetime.utcnow().isoformat()

        # Hash password if provided
        if "password" in user_data:
            user_data["password"] = get_password_hash(user_data["password"])

        data["users"].append(user_data)
        self._write_data(data)
        return user_data