```python
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from ..base import BaseRepository
from ...core.config import settings

class AnalyticsRepository(BaseRepository):
    def __init__(self):
        super().__init__(settings.DATA_FILE)

    def log_activity(self, activity_data: Dict) -> bool:
        data = self._read_data()
        if "analytics" not in data:
            data["analytics"] = []
        
        activity = {
            "timestamp": datetime.utcnow(),
            **activity_data
        }
        
        data["analytics"].append(activity)
        self._write_data(data)
        return True

    def get_user_analytics(self, user_id: str) -> Dict:
        data = self._read_data()
        activities = data.get("analytics", [])
        user_activities = [a for a in activities if a["user_id"] == user_id]
        
        # Calcular estadísticas
        total_sessions = len(set(a["session_id"] for a in user_activities if "session_id" in a))
        current_sessions = len(self.get_active_sessions(user_id))
        
        account_usage = {}
        for activity in user_activities:
            account_id = activity.get("account_id")
            if account_id:
                if account_id not in account_usage:
                    account_usage[account_id] = {
                        "total_time": 0,
                        "last_access": None,
                        "total_accesses": 0
                    }
                account_usage[account_id]["total_accesses"] += 1
                account_usage[account_id]["last_access"] = activity["timestamp"]

        return {
            "total_sessions": total_sessions,
            "current_sessions": current_sessions,
            "account_usage": list(account_usage.items()),
            "last_activities": sorted(user_activities, key=lambda x: x["timestamp"], reverse=True)[:10]
        }

    def get_account_analytics(self, account_id: int) -> Dict:
        data = self._read_data()
        activities = data.get("analytics", [])
        account_activities = [a for a in activities if a.get("account_id") == account_id]
        
        users = set(a["user_id"] for a in account_activities)
        active_users = set(
            a["user_id"] for a in account_activities 
            if (datetime.utcnow() - a["timestamp"]).total_seconds() < 3600
        )
        
        domain_usage = {}
        for activity in account_activities:
            domain = activity.get("domain")
            if domain:
                domain_usage[domain] = domain_usage.get(domain, 0) + 1

        return {
            "total_users": len(users),
            "active_users": len(active_users),
            "total_sessions": len(set(a["session_id"] for a in account_activities if "session_id" in a)),
            "domain_usage": domain_usage,
            "recent_activities": sorted(account_activities, key=lambda x: x["timestamp"], reverse=True)[:10]
        }

    def get_active_sessions(self, user_id: str) -> List[Dict]:
        data = self._read_data()
        sessions = data.get("sessions", [])
        timeout = datetime.utcnow() - timedelta(minutes=settings.SESSION_TIMEOUT_MINUTES)
        
        return [
            session for session in sessions
            if session["user_id"] == user_id and 
            datetime.fromisoformat(session["last_activity"]) > timeout
        ]

    def cleanup_old_analytics(self, days: int = 30) -> int:
        """Limpiar registros de análisis antiguos"""
        data = self._read_data()
        if "analytics" not in data:
            return 0
            
        cutoff = datetime.utcnow() - timedelta(days=days)
        initial_count = len(data["analytics"])
        
        data["analytics"] = [
            a for a in data["analytics"]
            if datetime.fromisoformat(a["timestamp"]) > cutoff
        ]
        
        self._write_data(data)
        return initial_count - len(data["analytics"])
```