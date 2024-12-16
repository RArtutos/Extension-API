from typing import List, Dict, Optional
from .base_service import BaseService

class GroupService(BaseService):
    def __init__(self):
        super().__init__('/api/groups')
    
    def get_all(self) -> List[Dict]:
        """Get all groups with their accounts"""
        try:
            result = self._handle_request('get', self.endpoint)
            return result if result else []
        except Exception as e:
            print(f"Error getting groups: {str(e)}")
            return []
    
    def create(self, data: Dict) -> Optional[Dict]:
        """Create a new group"""
        try:
            return self._handle_request('post', self.endpoint, data)
        except Exception as e:
            print(f"Error creating group: {str(e)}")
            return None

    def get_by_id(self, group_id: int) -> Optional[Dict]:
        """Get a specific group by ID"""
        try:
            return self._handle_request('get', f"{self.endpoint}/{group_id}")
        except Exception as e:
            print(f"Error getting group: {str(e)}")
            return None

    def assign_account(self, group_id: int, account_id: int) -> bool:
        """Assign an account to a group"""
        try:
            result = self._handle_request(
                'post', 
                f"{self.endpoint}/{group_id}/accounts/{account_id}"
            )
            return bool(result and result.get('message'))
        except Exception as e:
            print(f"Error assigning account to group: {str(e)}")
            return False