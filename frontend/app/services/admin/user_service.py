"""User management service module"""
from typing import List, Dict, Optional
from ..base_service import BaseService

class UserService(BaseService):
    def __init__(self):
        super().__init__('/api/admin/users')

    def get_all(self) -> List[Dict]:
        """Get all users"""
        try:
            return self._handle_request('get', '/api/admin/users') or []
        except Exception as e:
            print(f"Error fetching users: {str(e)}")
            return []

    def get_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        try:
            return self._handle_request('get', f"/api/admin/users/{user_id}")
        except Exception:
            return None

    def create(self, user_data: Dict) -> Optional[Dict]:
        """Create a new user"""
        try:
            if not user_data.get('email'):
                raise ValueError("Email is required")
                
            # Clean up preset_id if it's 0
            if user_data.get('preset_id') == 0:
                user_data['preset_id'] = None
                
            return self._handle_request('post', '/api/admin/users/create', user_data)
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return None

    def get_accounts(self, user_id: str) -> List[Dict]:
        """Get accounts assigned to a user"""
        try:
            return self._handle_request('get', f"/api/admin/users/{user_id}/accounts") or []
        except Exception:
            return []

    def get_available_accounts(self) -> List[Dict]:
        """Get all available accounts"""
        try:
            return self._handle_request('get', '/api/admin/accounts') or []
        except Exception:
            return []

    def assign_account(self, user_id: str, account_id: int) -> bool:
        """Assign account to user"""
        try:
            if not user_id or not isinstance(account_id, int):
                return False
            result = self._handle_request('post', f"/api/admin/users/{user_id}/accounts/{account_id}")
            return bool(result and result.get('success'))
        except Exception as e:
            print(f"Error assigning account: {str(e)}")
            return False

    def remove_account(self, user_id: str, account_id: int) -> bool:
        """Remove account from user"""
        try:
            if not user_id or not isinstance(account_id, int):
                return False
            result = self._handle_request('delete', f"/api/admin/users/{user_id}/accounts/{account_id}")
            return bool(result and result.get('success'))
        except Exception as e:
            print(f"Error removing account: {str(e)}")
            return False