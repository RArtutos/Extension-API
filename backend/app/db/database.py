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
        self._cleanup_inactive_sessions()
        data = self._read_data()
        accounts = data["accounts"]
        
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
            
        return accounts

    def update_user_activity(self, user_id: str, account_id: int, domain: str) -> bool:
        data = self._read_data()
        user_account = next(
            (ua for ua in data["user_accounts"] 
             if ua["user_id"] == user_id and ua["account_id"] == account_id),
            None
        )
        
        if not user_account:
            return False
            
        current_time = datetime.utcnow()
        user_account["last_activity"] = current_time.isoformat()
        
        # Log analytics
        data["analytics"].append({
            "user_id": user_id,
            "account_id": account_id,
            "domain": domain,
            "action": "access",
            "timestamp": current_time.isoformat()
        })
        
        self._write_data(data)
        return True

    def increment_session_count(self, user_id: str, account_id: int) -> bool:
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
            
        total_sessions = sum(
            ua["active_sessions"] for ua in data["user_accounts"]
            if ua["account_id"] == account_id
        )
        
        max_users = account.get("max_concurrent_users", settings.MAX_CONCURRENT_USERS_PER_ACCOUNT)
        if total_sessions >= max_users:
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

    def get_analytics(self, start_time: Optional[datetime] = None) -> Dict:
        data = self._read_data()
        if not start_time:
            start_time = datetime.utcnow() - timedelta(hours=24)
            
        analytics = [
            entry for entry in data["analytics"]
            if datetime.fromisoformat(entry["timestamp"]) > start_time
        ]
        
        return {
            "total_sessions": len(analytics),
            "active_accounts": len(set(entry["account_id"] for entry in analytics)),
            "active_users": len(set(entry["user_id"] for entry in analytics)),
            "recent_activity": sorted(
                analytics,
                key=lambda x: x["timestamp"],
                reverse=True
            )[:50]  # Last 50 activities
        }

    # ... (rest of the methods remain unchanged)


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
    
    # Generate new ID
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

def assign_group_to_account(self, account_id: int, group_id: int) -> bool:
    data = self._read_data()
    account = next((a for a in data["accounts"] if a["id"] == account_id), None)
    group = next((g for g in data.get("groups", []) if g["id"] == group_id), None)
    
    if not account or not group:
        return False
        
    account["group_id"] = group_id
    self._write_data(data)
    return True

def get_hourly_activity(self, start_time: datetime) -> List[Dict]:
    data = self._read_data()
    
    # Initialize hourly buckets
    hours = []
    current = start_time
    while current <= datetime.utcnow():
        hours.append({
            "hour": current.strftime("%H:00"),
            "timestamp": current.isoformat(),
            "count": 0
        })
        current += timedelta(hours=1)
    
    # Count activities per hour
    for activity in data["analytics"]:
        activity_time = datetime.fromisoformat(activity["timestamp"])
        if activity_time >= start_time:
            hour_index = int((activity_time - start_time).total_seconds() / 3600)
            if hour_index < len(hours):
                hours[hour_index]["count"] += 1
    
    return hours