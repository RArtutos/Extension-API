from datetime import datetime, timedelta
from typing import List, Dict
from ...db.analytics import AnalyticsDatabase

class UsageCalculator:
    def __init__(self):
        self.db = AnalyticsDatabase()

    def calculate_user_usage(self, user_id: str) -> Dict:
        """Calculate usage statistics for a user"""
        sessions = self.db.get_user_sessions(user_id)
        return {
            'total_time': self._calculate_total_time(sessions),
            'total_sessions': len(sessions),
            'current_sessions': len([s for s in sessions if s.get('active', False)]),
            'account_usage': self._calculate_account_usage(sessions)
        }

    def calculate_account_usage(self, account_id: int) -> Dict:
        """Calculate usage statistics for an account"""
        sessions = self.db.get_account_sessions(account_id)
        return {
            'total_sessions': len(sessions),
            'current_sessions': len([s for s in sessions if s.get('active', False)]),
            'usage_by_domain': self._calculate_domain_usage(sessions)
        }

    def _calculate_total_time(self, sessions: List[Dict]) -> int:
        """Calculate total time spent across all sessions"""
        return sum(s.get('duration', 0) for s in sessions)

    def _calculate_account_usage(self, sessions: List[Dict]) -> List[Dict]:
        """Calculate usage statistics per account"""
        account_stats = {}
        for session in sessions:
            account_id = session.get('account_id')
            if account_id not in account_stats:
                account_stats[account_id] = {
                    'total_time': 0,
                    'total_sessions': 0,
                    'last_activity': None
                }
            stats = account_stats[account_id]
            stats['total_sessions'] += 1
            stats['total_time'] += session.get('duration', 0)
            
            last_activity = session.get('last_activity')
            if last_activity:
                current = datetime.fromisoformat(last_activity)
                if not stats['last_activity'] or current > stats['last_activity']:
                    stats['last_activity'] = current
        
        return [{'account_id': k, **v} for k, v in account_stats.items()]

    def _calculate_domain_usage(self, sessions: List[Dict]) -> List[Dict]:
        """Calculate usage statistics per domain"""
        domain_stats = {}
        for session in sessions:
            domain = session.get('domain')
            if domain:
                if domain not in domain_stats:
                    domain_stats[domain] = {
                        'total_time': 0,
                        'total_sessions': 0
                    }
                stats = domain_stats[domain]
                stats['total_sessions'] += 1
                stats['total_time'] += session.get('duration', 0)
        
        return [{'domain': k, **v} for k, v in domain_stats.items()]