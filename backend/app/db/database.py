import json
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
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        data = self._read_data()
        user = next((user for user in data["users"] if user["email"] == email), None)
        if user:
            # Add assigned accounts
            user["assigned_accounts"] = [
                ua["account_id"] for ua in data["user_accounts"] 
                if ua["user_id"] == email
            ]
        return user

    def create_user(self, email: str, password: str, is_admin: bool = False) -> Dict:
        data = self._read_data()
        user = {
            "email": email,
            "password": get_password_hash(password),
            "is_admin": is_admin,
            "created_at": datetime.utcnow().isoformat(),
            "assigned_accounts": []
        }
        data["users"].append(user)
        self._write_data(data)
        return user

    def get_users(self) -> List[Dict]:
        data = self._read_data()
        users = data["users"]
        # Add assigned accounts to each user
        for user in users:
            user["assigned_accounts"] = [
                ua["account_id"] for ua in data["user_accounts"] 
                if ua["user_id"] == user["email"]
            ]
        return users

    # Account methods
    def get_accounts(self, user_email: Optional[str] = None) -> List[Dict]:
        data = self._read_data()
        accounts = data["accounts"]
        
        if user_email:
            user = self.get_user_by_email(user_email)
            if not user.get("is_admin"):
                user_accounts = [ua["account_id"] for ua in data["user_accounts"] 
                               if ua["user_id"] == user_email]
                accounts = [a for a in accounts if a["id"] in user_accounts]
            
        # Add session info to each account
        for account in accounts:
            account["active_sessions"] = sum(
                ua["active_sessions"] for ua in data["user_accounts"]
                if ua["account_id"] == account["id"]
            )
            account["max_concurrent_users"] = account.get("max_concurrent_users", 
                                                        settings.MAX_CONCURRENT_USERS_PER_ACCOUNT)
            
        return accounts

    def get_session_info(self, account_id: int) -> Dict:
        data = self._read_data()
        account = next((a for a in data["accounts"] if a["id"] == account_id), None)
        
        if not account:
            return {"active_sessions": 0, "max_concurrent_users": 0}
            
        active_sessions = sum(
            ua["active_sessions"] for ua in data["user_accounts"]
            if ua["account_id"] == account_id
        )
        
        return {
            "active_sessions": active_sessions,
            "max_concurrent_users": account.get("max_concurrent_users", 
                                              settings.MAX_CONCURRENT_USERS_PER_ACCOUNT)
        }

    def assign_account_to_user(self, user_id: str, account_id: int) -> bool:
        data = self._read_data()
        
        # Check if user and account exist
        user = self.get_user_by_email(user_id)
        account = next((a for a in data["accounts"] if a["id"] == account_id), None)
        
        if not user or not account:
            return False
            
        # Check if assignment already exists
        if any(ua["user_id"] == user_id and ua["account_id"] == account_id 
               for ua in data["user_accounts"]):
            return False
            
        # Create new assignment
        assignment = {
            "user_id": user_id,
            "account_id": account_id,
            "active_sessions": 0,
            "max_concurrent_users": account.get("max_concurrent_users", 1),
            "last_activity": None
        }
        
        data["user_accounts"].append(assignment)
        self._write_data(data)
        return True

    def remove_account_from_user(self, user_id: str, account_id: int) -> bool:
        data = self._read_data()
        initial_length = len(data["user_accounts"])
        
        data["user_accounts"] = [
            ua for ua in data["user_accounts"]
            if not (ua["user_id"] == user_id and ua["account_id"] == account_id)
        ]
        
        if len(data["user_accounts"]) < initial_length:
            self._write_data(data)
            return True
        return False