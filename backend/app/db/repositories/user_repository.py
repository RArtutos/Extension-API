from typing import List, Dict, Optional
from datetime import datetime
from .base_repository import BaseRepository
from ...core.auth import get_password_hash

class UserRepository(BaseRepository):
    def get_users(self) -> List[Dict]:
        data = self._read_data()
        users = data["users"]
        for user in users:
            user["assigned_accounts"] = [
                ua["account_id"] for ua in data["user_accounts"]
                if ua["user_id"] == user["email"]
            ]
        return users

    def create_user(self, email: str, password: str, is_admin: bool = False) -> Optional[Dict]:
        data = self._read_data()
        
        if any(user["email"] == email for user in data["users"]):
            return None
            
        user = {
            "email": email,
            "password": get_password_hash(password),
            "is_admin": is_admin,
            "created_at": datetime.utcnow().isoformat()
        }
        
        data["users"].append(user)
        self._write_data(data)
        return user

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        data = self._read_data()
        user = next((user for user in data["users"] if user["email"] == email), None)
        if user:
            user["assigned_accounts"] = [
                ua["account_id"] for ua in data["user_accounts"]
                if ua["user_id"] == email
            ]
        return user