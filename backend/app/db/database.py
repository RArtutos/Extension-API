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

    # User methods
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        data = self._read_data()
        return next((user for user in data["users"] if user["email"] == email), None)

    def create_user(self, email: str, password: str, is_admin: bool = False) -> Dict:
        data = self._read_data()
        
        if any(user["email"] == email for user in data["users"]):
            raise ValueError("Email already registered")
            
        user = {
            "email": email,
            "password": get_password_hash(password),
            "is_admin": is_admin,
            "created_at": datetime.utcnow().isoformat()
        }
        
        data["users"].append(user)
        self._write_data(data)
        return user

    def get_users(self) -> List[Dict]:
        data = self._read_data()
        return data["users"]

    # Group methods
    def get_groups(self) -> List[Dict]:
        data = self._read_data()
        if "groups" not in data:
            data["groups"] = []
            self._write_data(data)
        return data["groups"]

    def create_group(self, group_data: Dict) -> Dict:
        data = self._read_data()
        if "groups" not in data:
            data["groups"] = []
        
        new_id = max([g.get("id", 0) for g in data["groups"]], default=0) + 1
        
        group = {
            "id": new_id,
            "name": group_data["name"],
            "description": group_data.get("description", ""),
            "created_at": datetime.utcnow().isoformat()
        }
        
        data["groups"].append(group)
        self._write_data(data)
        return group

    def get_group_by_id(self, group_id: int) -> Optional[Dict]:
        data = self._read_data()
        return next((g for g in data.get("groups", []) if g["id"] == group_id), None)

    def get_accounts_by_group(self, group_id: int) -> List[Dict]:
        data = self._read_data()
        return [a for a in data["accounts"] if a.get("group_id") == group_id]

    def assign_group_to_account(self, account_id: int, group_id: int) -> bool:
        data = self._read_data()
        account = next((a for a in data["accounts"] if a["id"] == account_id), None)
        group = next((g for g in data.get("groups", []) if g["id"] == group_id), None)
        
        if not account or not group:
            return False
            
        account["group_id"] = group_id
        self._write_data(data)
        return True

    # Account methods
    def create_account(self, account_data: Dict) -> Optional[Dict]:
        data = self._read_data()
        
        new_id = max([a.get("id", 0) for a in data["accounts"]], default=0) + 1
        
        account = {
            "id": new_id,
            "name": account_data["name"],
            "group_id": account_data.get("group"),  # Changed from group to group_id
            "cookies": account_data.get("cookies", []),
            "max_concurrent_users": account_data.get("max_concurrent_users", 
                                                   settings.MAX_CONCURRENT_USERS_PER_ACCOUNT),
            "active_sessions": 0,
            "active_users": []
        }
        
        data["accounts"].append(account)
        self._write_data(data)
        return account

    def get_accounts(self, user_email: Optional[str] = None) -> List[Dict]:
        self._cleanup_inactive_sessions()
        data = self._read_data()
        accounts = data["accounts"]
        groups = {g["id"]: g["name"] for g in data.get("groups", [])}
        
        if user_email:
            user = self.get_user_by_email(user_email)
            if not user.get("is_admin"):
                user_accounts = [ua["account_id"] for ua in data["user_accounts"] 
                               if ua["user_id"] == user_email]
                accounts = [a for a in accounts if a["id"] in user_accounts]
            
        # Add session info and active users to each account
        for account in accounts:
            account_sessions = [
                ua for ua in data["user_accounts"]
                if ua["account_id"] == account["id"] and ua["active_sessions"] > 0
            ]
            
            account["active_sessions"] = sum(ua["active_sessions"] for ua in account_sessions)
            account["max_concurrent_users"] = account.get("max_concurrent_users", 
                                                        settings.MAX_CONCURRENT_USERS_PER_ACCOUNT)
            account["active_users"] = [
                {
                    "user_id": ua["user_id"],
                    "sessions": ua["active_sessions"],
                    "last_activity": ua["last_activity"]
                }
                for ua in account_sessions
            ]
            # Add group name if account has a group_id
            if account.get("group_id") and account["group_id"] in groups:
                account["group"] = groups[account["group_id"]]
            else:
                account["group"] = None
            
        return accounts

    def update_account(self, account_id: int, account_data: Dict) -> Optional[Dict]:
        data = self._read_data()
        account = next((a for a in data["accounts"] if a["id"] == account_id), None)
        
        if not account:
            return None
            
        account.update({
            "name": account_data["name"],
            "group_id": account_data.get("group"),  # Changed from group to group_id
            "cookies": account_data.get("cookies", []),
            "max_concurrent_users": account_data.get("max_concurrent_users", 
                                                   settings.MAX_CONCURRENT_USERS_PER_ACCOUNT)
        })
        
        self._write_data(data)
        return account

    def increment_session_count(self, user_id: str, account_id: int) -> bool:
        data = self._read_data()
        account = next((a for a in data["accounts"] if a["id"] == account_id), None)
        
        if not account:
            return False
            
        user_account = next(
            (ua for ua in data["user_accounts"] 
             if ua["user_id"] == user_id and ua["account_id"] == account_id),
            None
        )
        
        if not user_account:
            user_account = {
                "user_id": user_id,
                "account_id": account_id,
                "active_sessions": 0,
                "last_activity": None
            }
            data["user_accounts"].append(user_account)
            
        if user_account["active_sessions"] >= account["max_concurrent_users"]:
            return False
            
        user_account["active_sessions"] += 1
        user_account["last_activity"] = datetime.utcnow().isoformat()
        
        self._write_data(data)
        return True

    def decrement_session_count(self, user_id: str, account_id: int) -> bool:
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
        data = self._read_data()
        user_account = next(
            (ua for ua in data["user_accounts"] 
             if ua["user_id"] == user_id and ua["account_id"] == account_id),
            None
        )
        
        if not user_account or user_account["active_sessions"] <= 0:
            return False
            
        user_account["last_activity"] = datetime.utcnow().isoformat()
        
        # Add analytics entry
        if "analytics" not in data:
            data["analytics"] = []
            
        data["analytics"].append({
            "user_id": user_id,
            "account_id": account_id,
            "domain": domain,
            "timestamp": datetime.utcnow().isoformat(),
            "action": "access"
        })
        
        self._write_data(data)
        return True

    def get_analytics(self, start_time: datetime) -> Dict:
        data = self._read_data()
        current_time = datetime.utcnow()
        
        # Filter recent activity
        recent_activity = [
            a for a in data.get("analytics", [])
            if datetime.fromisoformat(a["timestamp"]) > start_time
        ]
        
        # Get active accounts and users
        active_accounts = len([
            a for a in data["accounts"]
            if any(ua["account_id"] == a["id"] and ua["active_sessions"] > 0
                  for ua in data["user_accounts"])
        ])
        
        active_users = len(set(
            ua["user_id"] for ua in data["user_accounts"]
            if ua["active_sessions"] > 0
        ))
        
        # Calculate total sessions
        total_sessions = sum(
            ua["active_sessions"] for ua in data["user_accounts"]
        )
        
        return {
            "total_sessions": total_sessions,
            "active_accounts": active_accounts,
            "active_users": active_users,
            "recent_activity": sorted(
                recent_activity,
                key=lambda x: x["timestamp"],
                reverse=True
            )[:50]  # Last 50 activities
        }

    def get_hourly_activity(self, start_time: datetime) -> List[Dict]:
        data = self._read_data()
        activities = data.get("analytics", [])
        
        # Group activities by hour
        hourly_counts = {}
        for activity in activities:
            timestamp = datetime.fromisoformat(activity["timestamp"])
            if timestamp > start_time:
                hour = timestamp.replace(minute=0, second=0, microsecond=0)
                hourly_counts[hour] = hourly_counts.get(hour, 0) + 1
                
        # Convert to list and sort
        return [
            {"hour": hour.isoformat(), "count": count}
            for hour, count in sorted(hourly_counts.items())
        ]