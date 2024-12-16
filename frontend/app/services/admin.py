from typing import List, Dict, Optional
from .base_service import BaseService

class AdminService(BaseService):
    def __init__(self):
        super().__init__('/api/admin')

    def get_users(self) -> List[Dict]:
        result = self._handle_request('get', f"{self.endpoint}/users")
        return result if result else []

    def create_user(self, data: Dict) -> Optional[Dict]:
        return self._handle_request('post', f"{self.endpoint}/users", data)

    def get_user(self, user_id: str) -> Optional[Dict]:
        users = self.get_users()
        return next((user for user in users if user['email'] == user_id), None)

    def get_analytics(self) -> Dict:
        result = self._handle_request('get', f"{self.endpoint}/analytics")
        return result if result else {'accounts': [], 'recent_activity': []}

    def get_user_accounts(self, user_id: str) -> List[Dict]:
        result = self._handle_request('get', f"{self.endpoint}/users/{user_id}/accounts")
        return result if result else []

    def get_available_accounts(self) -> List[Dict]:
        result = self._handle_request('get', "/api/accounts/")
        return result if result else []

    def assign_account_to_user(self, user_id: str, account_id: int) -> Optional[Dict]:
        return self._handle_request(
            'post', 
            f"{self.endpoint}/users/{user_id}/accounts/{account_id}"
        )