from typing import List, Dict, Optional
from .base_service import BaseService

class AdminService(BaseService):
    def __init__(self):
        super().__init__('/api/admin')

    def get_users(self) -> List[Dict]:
        result = self._handle_request('get', f"{self.endpoint}/users/")
        return result if result else []

    def get_analytics(self) -> Dict:
        """Get admin analytics dashboard data"""
        result = self._handle_request('get', f"{self.endpoint}/analytics")
        return result if result else {
            'accounts': [],
            'recent_activity': []
        }

    def get_user_analytics(self, user_id: str) -> Dict:
        """Get analytics for a specific user"""
        result = self._handle_request('get', f"{self.endpoint}/analytics/user/{user_id}")
        return result if result else {}

    def get_account_analytics(self, account_id: int) -> Dict:
        """Get analytics for a specific account"""
        result = self._handle_request('get', f"{self.endpoint}/analytics/account/{account_id}")
        return result if result else {}