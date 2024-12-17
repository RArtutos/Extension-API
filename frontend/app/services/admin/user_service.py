"""User management service"""
from typing import List, Dict, Optional
from ..base_service import BaseService
from ...utils.validators import validate_account_ids

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
        # Extract preset_id before creating user
        preset_id = user_data.pop('preset_id', None)
        if preset_id == 0:  # Handle case where '0' is selected as 'None'
            preset_id = None
            
        # Create user first
        user = self._handle_request('post', '/', user_data)
        
        if user and preset_id:
            try:
                from .preset_service import PresetService
                preset_service = PresetService()
                preset = preset_service.get_by_id(preset_id)
                
                if preset and preset.get('account_ids'):
                    # Assign each account from the preset
                    for account_id in preset['account_ids']:
                        self.assign_account(user['email'], account_id)
            except Exception as e:
                print(f"Error assigning preset accounts: {str(e)}")
                # Continue even if preset assignment fails
                pass
                
        return user

    def get_accounts(self, user_id: str) -> List[Dict]:
        """Get accounts assigned to a user"""
        return self._handle_request('get', f"/{user_id}/accounts") or []

    def assign_account(self, user_id: str, account_id: int) -> bool:
        """Assign an account to a user"""
        try:
            result = self._handle_request('post', f"/{user_id}/accounts/{account_id}")
            return bool(result and result.get('success'))
        except Exception as e:
            print(f"Error assigning account: {str(e)}")
            return False

    def remove_account(self, user_id: str, account_id: int) -> bool:
        """Remove an account from a user"""
        try:
            result = self._handle_request('delete', f"/{user_id}/accounts/{account_id}")
            return bool(result and result.get('success'))
        except Exception as e:
            print(f"Error removing account: {str(e)}")
            return False