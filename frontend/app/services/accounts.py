from typing import List, Dict, Optional
from .base_service import BaseService

class AccountService(BaseService):
    def __init__(self):
        super().__init__('/api/accounts')
    
    def get_all(self) -> List[Dict]:
        """Get all accounts with session information"""
        accounts = self._handle_request('get', self.endpoint + '/')
        if not accounts:
            return []
            
        # Get session info for each account
        for account in accounts:
            try:
                session_info = self._handle_request('get', f"{self.endpoint}/{account['id']}/session")
                account['active_sessions'] = session_info.get('active_sessions', 0)
                account['max_concurrent_users'] = session_info.get('max_concurrent_users', 1)
            except Exception:
                account['active_sessions'] = 0
                account['max_concurrent_users'] = 1
                
        return accounts
    
    def create(self, data: Dict) -> Optional[Dict]:
        return self._handle_request('post', self.endpoint + '/', data)
    
    def get_by_id(self, account_id: int) -> Optional[Dict]:
        return self._handle_request('get', f"{self.endpoint}/{account_id}")

    def update(self, account_id: int, data: Dict) -> Optional[Dict]:
        return self._handle_request('put', f"{self.endpoint}/{account_id}", data)

    def delete(self, account_id: int) -> bool:
        result = self._handle_request('delete', f"{self.endpoint}/{account_id}")
        return bool(result)
    
    def get_session_info(self, account_id: int) -> Dict:
        result = self._handle_request('get', f"{self.endpoint}/{account_id}/session")
        return result if result else {'active_sessions': 0, 'max_concurrent_users': 1}