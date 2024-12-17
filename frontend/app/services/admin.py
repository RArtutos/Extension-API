from typing import List, Dict, Optional
from .base_service import BaseService

class AdminService(BaseService):
    def __init__(self):
        super().__init__('/api/admin')

    def get_users(self) -> List[Dict]:
        result = self._handle_request('get', f"{self.endpoint}/users/")
        return result if result else []

    def create_user(self, data: Dict) -> Optional[Dict]:
        return self._handle_request('post', f"{self.endpoint}/users/", data)

    def get_user(self, user_id: str) -> Optional[Dict]:
        users = self.get_users()
        return next((user for user in users if user['email'] == user_id), None)

    def get_user_accounts(self, user_id: str) -> List[Dict]:
        result = self._handle_request('get', f"{self.endpoint}/users/{user_id}/accounts")
        return result if result else []

    def get_available_accounts(self) -> List[Dict]:
        result = self._handle_request('get', "/api/accounts/")
        return result if result else []

    def delete_user(self, user_id: str) -> bool:
        result = self._handle_request('delete', f"{self.endpoint}/users/{user_id}")
        return bool(result)

    # Preset management methods
    def get_presets(self) -> List[Dict]:
        result = self._handle_request('get', f"{self.endpoint}/presets/")
        return result if result else []

    def create_preset(self, data: Dict) -> Optional[Dict]:
        return self._handle_request('post', f"{self.endpoint}/presets/", data)

    def get_preset(self, preset_id: int) -> Optional[Dict]:
        return self._handle_request('get', f"{self.endpoint}/presets/{preset_id}")

    def update_preset(self, preset_id: int, data: Dict) -> Optional[Dict]:
        return self._handle_request('put', f"{self.endpoint}/presets/{preset_id}", data)

    def delete_preset(self, preset_id: int) -> bool:
        result = self._handle_request('delete', f"{self.endpoint}/presets/{preset_id}")
        return bool(result)