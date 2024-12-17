from datetime import datetime, timedelta
from typing import Optional, List, Dict
from ..core.config import settings
from ..core.auth import get_password_hash

class Database:
    def __init__(self):
        self.file_path = settings.DATA_FILE

    def _read_data(self) -> dict:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _write_data(self, data: dict):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)

    # User methods
    def get_users(self) -> List[Dict]:
        data = self._read_data()
        users = data.get("users", [])
        
        for user in users:
            if isinstance(user.get("created_at"), str):
                user["created_at"] = datetime.fromisoformat(user["created_at"])
            if user.get("expires_at") and isinstance(user["expires_at"], str):
                user["expires_at"] = datetime.fromisoformat(user["expires_at"])
            
            user["is_active"] = True
            if user.get("expires_at"):
                user["is_active"] = datetime.utcnow() < user["expires_at"]
            
            user["assigned_accounts"] = [
                ua["account_id"] for ua in data.get("user_accounts", [])
                if ua["user_id"] == user["email"]
            ]
        
        return users

    def create_user(self, email: str, password: str, is_admin: bool = False, 
                   expires_in_days: Optional[int] = None, preset_id: Optional[int] = None) -> Dict:
        data = self._read_data()
        
        expires_at = None
        if expires_in_days is not None:
            expires_at = (datetime.utcnow() + timedelta(days=expires_in_days)).isoformat()

        user = {
            "email": email,
            "password": get_password_hash(password),
            "is_admin": is_admin,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": expires_at,
            "preset_id": preset_id,
            "assigned_accounts": []
        }
        
        data["users"].append(user)
        self._write_data(data)

        if preset_id is not None:
            preset = self.get_preset(preset_id)
            if preset:
                for account_id in preset["account_ids"]:
                    self.assign_account_to_user(email, account_id)

        return user