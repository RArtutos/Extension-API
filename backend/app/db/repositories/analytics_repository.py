from typing import List, Dict, Optional
from datetime import datetime, timedelta
from ..base import BaseRepository
from ...core.config import settings

class AnalyticsRepository(BaseRepository):
    def __init__(self):
        super().__init__(settings.DATA_FILE)

    def get_recent_activities(self, limit: int = 10) -> List[Dict]:
        data = self._read_data()
        activities = data.get("analytics", [])
        
        # Sort by timestamp descending and limit
        sorted_activities = sorted(
            activities,
            key=lambda x: x.get("timestamp", ""),
            reverse=True
        )
        return sorted_activities[:limit]

    def get_account_sessions(self, account_id: int) -> List[Dict]:
        data = self._read_data()
        return [
            s for s in data.get("sessions", [])
            if s.get("account_id") == account_id
        ]

    def get_user_sessions(self, user_id: str) -> List[Dict]:
        data = self._read_data()
        return [
            s for s in data.get("sessions", [])
            if s.get("user_id") == user_id
        ]

    def get_account_users(self, account_id: int) -> List[Dict]:
        data = self._read_data()
        user_accounts = [
            ua for ua in data.get("user_accounts", [])
            if ua.get("account_id") == account_id
        ]
        user_ids = [ua.get("user_id") for ua in user_accounts]
        return [
            u for u in data.get("users", [])
            if u.get("email") in user_ids
        ]

    def get_accounts(self) -> List[Dict]:
        data = self._read_data()
        return data.get("accounts", [])