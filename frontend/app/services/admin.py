"""Admin service module"""
from typing import List, Dict, Optional
from .base_service import BaseService

class AdminService(BaseService):
    def __init__(self):
        super().__init__('/api/admin')

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