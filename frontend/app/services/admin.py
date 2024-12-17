"""Admin service module for managing administrative operations"""
from typing import List, Dict, Optional
from .base_service import BaseService

class AdminService(BaseService):
    def __init__(self):
        super().__init__('/api/admin')

    def get_users(self) -> List[Dict]:
        """Get all users"""
        result = self._handle_request('get', f"{self.endpoint}/users")
        return result if result else []

    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get a specific user"""
        users = self.get_users()
        return next((user for user in users if user['email'] == user_id), None)

    def create_user(self, user_data: Dict) -> Optional[Dict]:
        """Create a new user"""
        return self._handle_request('post', f"{self.endpoint}/users", user_data)

    def get_user_accounts(self, user_id: str) -> List[Dict]:
        """Get accounts for a specific user"""
        result = self._handle_request('get', f"{self.endpoint}/users/{user_id}/accounts")
        return result if result else []

    def get_available_accounts(self) -> List[Dict]:
        """Get all available accounts"""
        result = self._handle_request('get', f"{self.endpoint}/accounts")
        return result if result else []

    def get_analytics(self) -> Dict:
        """Get admin analytics dashboard data"""
        result = self._handle_request('get', f"{self.endpoint}/analytics")
        return result if result else {
            'accounts': [],
            'recent_activity': []
        }