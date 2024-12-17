from typing import Dict
from .base_service import BaseService

class AnalyticsService(BaseService):
    def __init__(self):
        super().__init__('/api/analytics')
    
    def get_user_analytics(self, user_id: str) -> Dict:
        result = self._handle_request('get', f"/user/{user_id}")
        return result if result else {
            'current_sessions': 0,
            'total_time': 0,
            'total_sessions': 0,
            'account_usage': [],
            'last_activities': []
        }
    
    def get_account_analytics(self, account_id: int) -> Dict:
        result = self._handle_request('get', f"/account/{account_id}")
        return result if result else {
            'total_users': 0,
            'active_users': 0,
            'total_sessions': 0,
            'current_sessions': 0,
            'usage_by_domain': [],
            'user_activities': []
        }
        
    def get_dashboard_analytics(self) -> Dict:
        result = self._handle_request('get', '/api/admin/analytics')
        return result if result else {
            'accounts': [],
            'recent_activity': []
        }