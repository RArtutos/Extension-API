from typing import Dict, Optional
from datetime import datetime, timedelta
from .base_repository import BaseRepository

class SessionRepository(BaseRepository):
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
        
        if not user_account:
            return False
            
        user_account["last_activity"] = datetime.utcnow().isoformat()
        self._write_data(data)
        return True