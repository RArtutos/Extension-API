from typing import Dict, List
from datetime import datetime, timedelta
from ..db.database import Database

class AnalyticsManager:
    def __init__(self):
        self.db = Database()

    def get_dashboard_data(self) -> Dict:
        """Get general analytics dashboard data"""
        accounts = self.db.get_accounts()
        recent_activity = self.db.get_recent_activities(limit=10)
        
        return {
            "accounts": [{
                "id": acc["id"],
                "name": acc["name"],
                "active_sessions": len([s for s in self.db.get_account_sessions(acc["id"]) if s["active"]])
            } for acc in accounts],
            "recent_activity": recent_activity
        }

    def get_user_analytics(self, user_id: str) -> Dict:
        """Get analytics for a specific user"""
        sessions = self.db.get_user_sessions(user_id)
        account_usage = self.db.get_user_account_usage(user_id)
        
        return {
            "user_id": user_id,
            "total_time": sum(s["duration"] for s in sessions if s.get("duration")),
            "total_sessions": len(sessions),
            "current_sessions": len([s for s in sessions if s["active"]]),
            "last_activity": max((s["last_activity"] for s in sessions), default=None),
            "account_usage": account_usage
        }

    def get_account_analytics(self, account_id: int) -> Dict:
        """Get analytics for a specific account"""
        sessions = self.db.get_account_sessions(account_id)
        users = self.db.get_account_users(account_id)
        
        return {
            "account_id": account_id,
            "total_users": len(users),
            "active_users": len([u for u in users if u["active"]]),
            "total_sessions": len(sessions),
            "current_sessions": len([s for s in sessions if s["active"]]),
            "usage_by_domain": self._aggregate_domain_usage(sessions),
            "user_activities": self._get_recent_activities(account_id)
        }

    def _aggregate_domain_usage(self, sessions: List[Dict]) -> List[Dict]:
        """Aggregate usage statistics by domain"""
        domain_stats = {}
        for session in sessions:
            domain = session.get("domain")
            if domain:
                if domain not in domain_stats:
                    domain_stats[domain] = {
                        "total_time": 0,
                        "total_sessions": 0
                    }
                domain_stats[domain]["total_sessions"] += 1
                if session.get("duration"):
                    domain_stats[domain]["total_time"] += session["duration"]
        
        return [{"domain": k, **v} for k, v in domain_stats.items()]

    def _get_recent_activities(self, account_id: int) -> List[Dict]:
        """Get recent activities for an account"""
        return self.db.get_account_activities(account_id, limit=10)