from typing import List, Dict
from .base_service import BaseService

class AdminService(BaseService):
    def __init__(self):
        super().__init__('/api/admin')

    def get_users(self) -> List[Dict]:
        result = self._handle_request('get', f"{self.endpoint}/users")
        return result if result else []

    def create_user(self, data: Dict) -> Optional[Dict]:
        return self._handle_request('post', f"{self.endpoint}/users", data)

    def get_analytics(self) -> Dict:
        result = self._handle_request('get', f"{self.endpoint}/analytics")
        return result if result else {'accounts': [], 'recent_activity': []}

    def assign_account_to_user(self, user_id: str, account_id: int) -> Optional[Dict]:
        return self._handle_request(
            'post', 
            f"{self.endpoint}/users/{user_id}/accounts/{account_id}"
        )