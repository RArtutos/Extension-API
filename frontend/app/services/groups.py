from typing import List, Dict, Optional
from .base_service import BaseService

class GroupService(BaseService):
    def __init__(self):
        super().__init__('/api/groups')
    
    def get_all(self) -> List[Dict]:
        result = self._handle_request('get', self.endpoint)
        return result if result else []
    
    def create(self, data: Dict) -> Optional[Dict]:
        try:
            return self._handle_request('post', self.endpoint, data)
        except Exception as e:
            print(f"Error creating group: {str(e)}")
            raise
    
    def get_by_id(self, group_id: int) -> Optional[Dict]:
        result = self._handle_request('get', f"{self.endpoint}/{group_id}")
        return result if result else None
    
    def assign_account(self, group_id: int, account_id: int) -> bool:
        try:
            result = self._handle_request(
                'post', 
                f"{self.endpoint}/{group_id}/accounts/{account_id}"
            )
            return bool(result and result.get('message'))
        except Exception as e:
            print(f"Error assigning account to group: {str(e)}")
            raise