"""Preset management service"""
from typing import List, Dict, Optional
from ..base_service import BaseService

class PresetService(BaseService):
    def __init__(self):
        super().__init__('/api/admin/presets')

    def get_all(self) -> List[Dict]:
        """Get all presets"""
        return self._handle_request('get', '/') or []

    def get_by_id(self, preset_id: int) -> Optional[Dict]:
        """Get preset by ID"""
        return self._handle_request('get', f"/{preset_id}")

    def create(self, preset_data: Dict) -> Optional[Dict]:
        """Create a new preset"""
        return self._handle_request('post', '/', preset_data)

    def update(self, preset_id: int, preset_data: Dict) -> Optional[Dict]:
        """Update an existing preset"""
        return self._handle_request('put', f"/{preset_id}", preset_data)

    def delete(self, preset_id: int) -> bool:
        """Delete a preset"""
        result = self._handle_request('delete', f"/{preset_id}")
        return bool(result and result.get('success'))