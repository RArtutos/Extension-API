"""Admin service module"""
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

    def get_user_accounts(self, user_id: str) -> List[Dict]:
        """Get accounts assigned to a user"""
        result = self._handle_request('get', f"{self.endpoint}/users/{user_id}/accounts")
        return result if result else []

    def get_available_accounts(self) -> List[Dict]:
        """Get all available accounts"""
        result = self._handle_request('get', f"{self.endpoint}/accounts")
        return result if result else []

    def assign_account_to_user(self, user_id: str, account_id: int) -> bool:
        """Assign an account to a user"""
        result = self._handle_request(
            'post', 
            f"{self.endpoint}/users/{user_id}/accounts/{account_id}"
        )
        return bool(result)

    def remove_account_from_user(self, user_id: str, account_id: int) -> bool:
        """Remove an account from a user"""
        result = self._handle_request(
            'delete', 
            f"{self.endpoint}/users/{user_id}/accounts/{account_id}"
        )
        return bool(result)

    # ... resto del código existente ...