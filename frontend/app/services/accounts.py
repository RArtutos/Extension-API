from typing import List, Dict, Optional
from .base_service import BaseService

class AccountService(BaseService):
    def __init__(self):
        super().__init__('/api/accounts')
    
    def get_all(self) -> List[Dict]:
        result = self._handle_request('get', self.endpoint)
        return result if result else []
    
    def create(self, data: Dict) -> Optional[Dict]:
        return self._handle_request('post', self.endpoint, data)
    
    def get_by_id(self, account_id: int) -> Optional[Dict]:
        return self._handle_request('get', f"{self.endpoint}/{account_id}")

    def update(self, account_id: int, data: Dict) -> Optional[Dict]:
        return self._handle_request('put', f"{self.endpoint}/{account_id}", data)

    def delete(self, account_id: int) -> bool:
        result = self._handle_request('delete', f"{self.endpoint}/{account_id}")
        return bool(result)
    
    def get_session_info(self, account_id: int) -> Dict:
        result = self._handle_request('get', f"{self.endpoint}/{account_id}/session")
        return result if result else {'active_sessions': 0, 'max_concurrent_users': 0}

    def get_analytics(self, account_id: Optional[int] = None) -> List[Dict]:
        params = {'account_id': account_id} if account_id else None
        result = self._handle_request('get', '/api/admin/analytics', params)
        return result if result else []