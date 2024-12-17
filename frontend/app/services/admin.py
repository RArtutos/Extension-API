from typing import List, Dict, Optional
from .base_service import BaseService

class AdminService(BaseService):
    def __init__(self):
        super().__init__('/api/admin')

    def create_user(self, user_data: Dict) -> Optional[Dict]:
        """Create a new user"""
        return self._handle_request('post', f"{self.endpoint}/users", user_data)

    def get_users(self) -> List[Dict]:
        result = self._handle_request('get', f"{self.endpoint}/users/")
        return result if result else []

    def get_presets(self) -> List[Dict]:
        """Get all presets"""
        result = self._handle_request('get', f"{self.endpoint}/presets")
        return result if result else []

    def get_preset(self, preset_id: int) -> Optional[Dict]:
        """Get a specific preset"""
        result = self._handle_request('get', f"{self.endpoint}/presets/{preset_id}")
        return result if result else None

    def create_preset(self, preset_data: Dict) -> Optional[Dict]:
        """Create a new preset"""
        return self._handle_request('post', f"{self.endpoint}/presets", preset_data)

    def update_preset(self, preset_id: int, preset_data: Dict) -> Optional[Dict]:
        """Update an existing preset"""
        return self._handle_request('put', f"{self.endpoint}/presets/{preset_id}", preset_data)

    def delete_preset(self, preset_id: int) -> bool:
        """Delete a preset"""
        result = self._handle_request('delete', f"{self.endpoint}/presets/{preset_id}")
        return bool(result)

    def get_analytics(self) -> Dict:
        """Get admin analytics dashboard data"""
        result = self._handle_request('get', f"{self.endpoint}/analytics")
        return result if result else {
            'accounts': [],
            'recent_activity': []
        }

    def get_user_analytics(self, user_id: str) -> Dict:
        """Get analytics for a specific user"""
        result = self._handle_request('get', f"{self.endpoint}/analytics/user/{user_id}")
        return result if result else {}

    def get_account_analytics(self, account_id: int) -> Dict:
        """Get analytics for a specific account"""
        result = self._handle_request('get', f"{self.endpoint}/analytics/account/{account_id}")
        return result if result else {}