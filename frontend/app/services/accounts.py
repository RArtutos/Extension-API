from typing import List, Dict, Optional
from .base_service import BaseService

class AccountService(BaseService):
    def __init__(self):
        super().__init__('/api/accounts')
    
    def get_all(self) -> List[Dict]:
        result = self._handle_request('get', self.endpoint)
        return result if result else []
    
    def create(self, data: Dict) -> Optional[Dict]:
        try:
            return self._handle_request('post', self.endpoint, data)
        except Exception as e:
            print(f"Error creating account: {str(e)}")
            raise
    
    def get_by_id(self, account_id: int) -> Optional[Dict]:
        return self._handle_request('get', f"{self.endpoint}/{account_id}")

    def update(self, account_id: int, data: Dict) -> Optional[Dict]:
        try:
            return self._handle_request('put', f"{self.endpoint}/{account_id}", data)
        except Exception as e:
            print(f"Error updating account: {str(e)}")
            raise

    def delete(self, account_id: int) -> bool:
        try:
            result = self._handle_request('delete', f"{self.endpoint}/{account_id}")
            return bool(result)
        except Exception as e:
            print(f"Error deleting account: {str(e)}")
            raise