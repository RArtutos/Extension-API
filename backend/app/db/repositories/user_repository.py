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
            user["is_active"] = True if not user.get("expires_at") else datetime.utcnow() < user["expires_at"]
            user["max_devices"] = user.get("max_devices", 1)
            user["active_sessions"] = len([s for s in data.get("sessions", []) 
                                         if s["user_id"] == user["email"] and s.get("active", True)])
            user["assigned_accounts"] = [
                ua["account_id"] for ua in data.get("user_accounts", [])
                if ua["user_id"] == user["email"]
            ]
        
        return users

    def get_by_email(self, email: str) -> Optional[Dict]:
        data = self._read_data()
        user = next((user for user in data.get("users", []) if user["email"] == email), None)
        
        if user:
            if user.get("expires_at"):
                expires_at = datetime.fromisoformat(user["expires_at"])
                if datetime.utcnow() > expires_at:
                    return None
            
            # Add required fields
            user["max_devices"] = user.get("max_devices", 1)
            user["active_sessions"] = len([s for s in data.get("sessions", []) 
                                         if s["user_id"] == email and s.get("active", True)])
            user["assigned_accounts"] = [
                ua["account_id"] for ua in data.get("user_accounts", [])
                if ua["user_id"] == email
            ]
            
        return user