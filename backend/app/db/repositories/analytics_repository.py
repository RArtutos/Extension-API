from typing import Dict, List
from datetime import datetime, timedelta
from .base_repository import BaseRepository

class AnalyticsRepository(BaseRepository):
    def get_analytics(self, start_time: datetime) -> Dict:
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

    def log_activity(self, user_id: str, account_id: int, domain: str, action: str) -> None:
        data = self._read_data()
        
        log_entry = {
            "user_id": user_id,
            "account_id": account_id,
            "domain": domain,
            "action": action,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        data["analytics"].append(log_entry)
        self._write_data(data)