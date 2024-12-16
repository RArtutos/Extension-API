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

    # User Management Methods
    def get_users(self) -> List[Dict]:
        """Get all users"""
        data = self._read_data()
        users = data["users"]
        for user in users:
            user["assigned_accounts"] = [
                ua["account_id"] for ua in data["user_accounts"]
                if ua["user_id"] == user["email"]
            ]
        return users

    def create_user(self, email: str, password: str, is_admin: bool = False) -> Optional[Dict]:
        """Create a new user"""
        data = self._read_data()
        
        # Check if user already exists
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
        """Get user by email"""
        data = self._read_data()
        user = next((user for user in data["users"] if user["email"] == email), None)
        if user:
            # Add assigned accounts
            user["assigned_accounts"] = [
                ua["account_id"] for ua in data["user_accounts"]
                if ua["user_id"] == email
            ]
        return user

    # Account Management Methods
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

    def assign_account_to_user(self, user_id: str, account_id: int) -> bool:
        """Assign an account to a user"""
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
        """Remove an account from a user"""
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

    # Group Management Methods
    def get_groups(self) -> List[Dict]:
        """Get all groups with their accounts"""
        data = self._read_data()
        groups = data.get("groups", [])
        for group in groups:
            group["accounts"] = [
                a for a in data["accounts"]
                if a.get("group_id") == group["id"]
            ]
        return groups

    def get_group_by_id(self, group_id: int) -> Optional[Dict]:
        """Get a group by its ID"""
        data = self._read_data()
        group = next((g for g in data.get("groups", []) if g["id"] == group_id), None)
        if group:
            group["accounts"] = [
                a for a in data["accounts"]
                if a.get("group_id") == group["id"]
            ]
        return group

    def create_group(self, name: str, description: str = "") -> Optional[Dict]:
        """Create a new group"""
        data = self._read_data()
        if "groups" not in data:
            data["groups"] = []
            
        new_id = max([g.get("id", 0) for g in data["groups"]], default=0) + 1
        group = {
            "id": new_id,
            "name": name,
            "description": description,
            "created_at": datetime.utcnow().isoformat()
        }
        
        data["groups"].append(group)
        self._write_data(data)
        return group

    def assign_group_to_user(self, user_id: str, group_id: int) -> bool:
        """Assign all accounts from a group to a user"""
        data = self._read_data()
        
        # Verify group exists
        group = self.get_group_by_id(group_id)
        if not group:
            return False
            
        # Get all accounts in the group
        group_accounts = [a["id"] for a in data["accounts"] if a.get("group_id") == group_id]
        
        # Assign each account to the user
        success = True
        for account_id in group_accounts:
            if not self.assign_account_to_user(user_id, account_id):
                success = False
                
        return success

    # Session Management Methods
    def increment_session_count(self, user_id: str, account_id: int) -> bool:
        """Increment session count for user-account pair"""
        data = self._read_data()
        user_account = next(
            (ua for ua in data["user_accounts"]
             if ua["user_id"] == user_id and ua["account_id"] == account_id),
            None
        )
        
        if not user_account:
            return False
            
        account = next((a for a in data["accounts"] if a["id"] == account_id), None)
        if not account:
            return False
            
        if user_account["active_sessions"] >= account["max_concurrent_users"]:
            return False
            
        user_account["active_sessions"] += 1
        user_account["last_activity"] = datetime.utcnow().isoformat()
        self._write_data(data)
        return True

    def decrement_session_count(self, user_id: str, account_id: int) -> bool:
        """Decrement session count for user-account pair"""
        data = self._read_data()
        user_account = next(
            (ua for ua in data["user_accounts"]
             if ua["user_id"] == user_id and ua["account_id"] == account_id),
            None
        )
        
        if not user_account or user_account["active_sessions"] <= 0:
            return False
            
        user_account["active_sessions"] -= 1
        if user_account["active_sessions"] == 0:
            user_account["last_activity"] = None
        self._write_data(data)
        return True

    def update_user_activity(self, user_id: str, account_id: int, domain: str) -> bool:
        """Update user activity timestamp and log analytics"""
        data = self._read_data()
        user_account = next(
            (ua for ua in data["user_accounts"]
             if ua["user_id"] == user_id and ua["account_id"] == account_id),
            None
        )
        
        if not user_account:
            return False
            
        current_time = datetime.utcnow().isoformat()
        user_account["last_activity"] = current_time
        
        # Log analytics
        data["analytics"].append({
            "user_id": user_id,
            "account_id": account_id,
            "domain": domain,
            "timestamp": current_time,
            "action": "access"
        })
        
        self._write_data(data)
        return True

    # Analytics Methods
    def get_analytics(self, start_time: datetime) -> Dict:
        """Get analytics data from start_time"""
        data = self._read_data()
        recent_logs = [
            log for log in data["analytics"]
            if datetime.fromisoformat(log["timestamp"]) >= start_time
        ]
        
        return {
            "total_sessions": sum(ua["active_sessions"] for ua in data["user_accounts"]),
            "active_accounts": len([ua for ua in data["user_accounts"] if ua["active_sessions"] > 0]),
            "active_users": len(set(ua["user_id"] for ua in data["user_accounts"] if ua["active_sessions"] > 0)),
            "recent_activity": recent_logs
        }