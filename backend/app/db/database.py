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

    def _cleanup_inactive_sessions(self):
        data = self._read_data()
        current_time = datetime.utcnow()
        timeout = timedelta(minutes=2)  # 2 minutes inactivity timeout

        for user_account in data["user_accounts"]:
            if user_account.get("last_activity"):
                last_activity = datetime.fromisoformat(user_account["last_activity"])
                if current_time - last_activity > timeout:
                    user_account["active_sessions"] = 0
                    user_account["last_activity"] = None

        self._write_data(data)

    def get_user_accounts(self, user_id: str) -> List[Dict]:
        """Get all accounts assigned to a user"""
        data = self._read_data()
        user_accounts = [
            ua["account_id"] for ua in data["user_accounts"]
            if ua["user_id"] == user_id
        ]
        accounts = [
            account for account in data["accounts"]
            if account["id"] in user_accounts
        ]
        
        # Add group names to accounts
        groups = {g["id"]: g["name"] for g in data.get("groups", [])}
        for account in accounts:
            if account.get("group_id") and account["group_id"] in groups:
                account["group"] = groups[account["group_id"]]
            else:
                account["group"] = None
                
        return accounts

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        data = self._read_data()
        user = next((user for user in data["users"] if user["email"] == email), None)
        if user:
            # Add assigned accounts
            user_accounts = [
                ua["account_id"] for ua in data["user_accounts"]
                if ua["user_id"] == email
            ]
            user["assigned_accounts"] = user_accounts
        return user

    def assign_account_to_user(self, user_id: str, account_id: int) -> bool:
        data = self._read_data()
        
        # Verify user exists
        user = self.get_user_by_email(user_id)
        if not user:
            return False
            
        # Verify account exists
        account = next((a for a in data["accounts"] if a["id"] == account_id), None)
        if not account:
            return False
            
        # Create user_account entry if it doesn't exist
        user_account = next(
            (ua for ua in data["user_accounts"] 
             if ua["user_id"] == user_id and ua["account_id"] == account_id),
            None
        )
        
        if not user_account:
            data["user_accounts"].append({
                "user_id": user_id,
                "account_id": account_id,
                "active_sessions": 0,
                "last_activity": None
            })
            self._write_data(data)
            
        return True

    def remove_account_from_user(self, user_id: str, account_id: int) -> bool:
        data = self._read_data()
        initial_length = len(data["user_accounts"])
        
        data["user_accounts"] = [
            ua for ua in data["user_accounts"]
            if not (ua["user_id"] == user_id and ua["account_id"] == account_id)
        ]
        
        if len(data["user_accounts"]) != initial_length:
            self._write_data(data)
            return True
        return False