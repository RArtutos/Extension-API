"""Admin service module"""
from typing import List, Dict, Optional
from .base_service import BaseService

class AdminService(BaseService):
    def __init__(self):
        super().__init__('/api/admin')

    def get_users(self) -> List[Dict]:
        """Get all users"""
        return self._handle_request('get', f"{self.endpoint}/users") or []

    def create_user(self, user_data: Dict) -> Optional[Dict]:
        """Create a new user"""
        # Extract preset_id before creating user
        preset_id = user_data.pop('preset_id', None)
        if preset_id == 0:  # Handle case where '0' is selected as 'None'
            preset_id = None
            
        # Create user first
        user = self._handle_request('post', f"{self.endpoint}/users", user_data)
        
        if user and preset_id:
            try:
                # Get preset accounts
                preset = self.get_preset(preset_id)
                if preset and preset.get('account_ids'):
                    # Assign each account from the preset
                    for account_id in preset['account_ids']:
                        self.assign_account_to_user(user['email'], account_id)
            except Exception as e:
                print(f"Error assigning preset accounts: {str(e)}")
                # Continue even if preset assignment fails
                pass
                
        return user

    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        return self._handle_request('get', f"{self.endpoint}/users/{user_id}")

    def get_user_accounts(self, user_id: str) -> List[Dict]:
        """Get accounts assigned to a user"""
        return self._handle_request('get', f"{self.endpoint}/users/{user_id}/accounts") or []

    def get_available_accounts(self) -> List[Dict]:
        """Get all available accounts"""
        return self._handle_request('get', f"{self.endpoint}/accounts") or []

    def assign_account_to_user(self, user_id: str, account_id: int) -> bool:
        """Assign an account to a user"""
        try:
            result = self._handle_request(
                'post', 
                f"{self.endpoint}/users/{user_id}/accounts/{account_id}"
            )
            return bool(result and result.get('success'))
        except Exception as e:
            print(f"Error assigning account: {str(e)}")
            return False

    def remove_account_from_user(self, user_id: str, account_id: int) -> bool:
        """Remove an account from a user"""
        try:
            result = self._handle_request(
                'delete',
                f"{self.endpoint}/users/{user_id}/accounts/{account_id}"
            )
            return bool(result and result.get('success'))
        except Exception as e:
            print(f"Error removing account: {str(e)}")
            return False

    def get_presets(self) -> List[Dict]:
        """Get all presets"""
        return self._handle_request('get', f"{self.endpoint}/presets") or []

    def get_preset(self, preset_id: int) -> Optional[Dict]:
        """Get preset by ID"""
        return self._handle_request('get', f"{self.endpoint}/presets/{preset_id}")

    def create_preset(self, preset_data: Dict) -> Optional[Dict]:
        """Create a new preset"""
        return self._handle_request('post', f"{self.endpoint}/presets", preset_data)

    def update_preset(self, preset_id: int, preset_data: Dict) -> Optional[Dict]:
        """Update an existing preset"""
        return self._handle_request('put', f"{self.endpoint}/presets/{preset_id}", preset_data)

    def delete_preset(self, preset_id: int) -> bool:
        """Delete a preset"""
        result = self._handle_request('delete', f"{self.endpoint}/presets/{preset_id}")
        return bool(result and result.get('success'))

    def get_analytics(self) -> Dict:
        """Get analytics dashboard data"""
        return self._handle_request('get', f"{self.endpoint}/analytics") or {
            'accounts': [],
            'recent_activity': []
        }

    def get_user_analytics(self, user_id: str) -> Dict:
        """Get analytics for a specific user"""
        return self._handle_request('get', f"{self.endpoint}/analytics/user/{user_id}") or {}

    def get_account_analytics(self, account_id: int) -> Dict:
        """Get analytics for a specific account"""
        return self._handle_request('get', f"{self.endpoint}/analytics/account/{account_id}") or {}