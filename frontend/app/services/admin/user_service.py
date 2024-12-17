"""User management service module"""
from typing import List, Dict, Optional
from ..base_service import BaseService

class UserService(BaseService):
    def __init__(self):
        super().__init__('/api/admin/users')

    def get_all(self) -> List[Dict]:
        """Get all users"""
        return self._handle_request('get', '/') or []

    def get_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        return self._handle_request('get', f"/{user_id}")

    def create(self, user_data: Dict) -> Optional[Dict]:
        """Create a new user"""
        # Handle preset_id
        if user_data.get('preset_id') == 0:
            user_data['preset_id'] = None
            
        # Create user with preset information
        return self._handle_request('post', '/', user_data)

    def get_accounts(self, user_id: str) -> List[Dict]:
        """Get accounts assigned to a user"""
        return self._handle_request('get', f"/{user_id}/accounts") or []

    def get_available_accounts(self) -> List[Dict]:
        """Get all available accounts"""
        return self._handle_request('get', '/accounts') or []

    def assign_account(self, user_id: str, account_id: int) -> bool:
        """Assign account to user"""
        try:
            result = self._handle_request('post', f"/{user_id}/accounts/{account_id}")
            return bool(result and result.get('success'))
        except Exception as e:
            print(f"Error assigning account: {str(e)}")
            return False

    def remove_account(self, user_id: str, account_id: int) -> bool:
        """Remove account from user"""
        try:
            result = self._handle_request('delete', f"/{user_id}/accounts/{account_id}")
            return bool(result and result.get('success'))
        except Exception as e:
            print(f"Error removing account: {str(e)}")
            return False