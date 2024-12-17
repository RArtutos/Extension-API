"""Analytics service for admin functionality"""
from typing import Dict
from ..base_service import BaseService

class AnalyticsService(BaseService):
    def __init__(self):
        super().__init__('/api/admin/analytics')

    def get_dashboard(self) -> Dict:
        """Get analytics dashboard data"""
        return self._handle_request('get', '/') or {
            'accounts': [],
            'recent_activity': []
        }

    def get_user_analytics(self, user_id: str) -> Dict:
        """Get analytics for a specific user"""
        return self._handle_request('get', f"/user/{user_id}") or {}

    def get_account_analytics(self, account_id: int) -> Dict:
        """Get analytics for a specific account"""
        return self._handle_request('get', f"/account/{account_id}") or {}