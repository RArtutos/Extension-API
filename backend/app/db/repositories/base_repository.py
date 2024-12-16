from typing import Dict, Optional
import json
from ...core.config import settings

class BaseRepository:
    def __init__(self):
        self.file_path = settings.DATA_FILE

    def _read_data(self) -> dict:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _write_data(self, data: dict):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _get_next_id(self, collection: str) -> int:
        data = self._read_data()
        return max([item.get('id', 0) for item in data.get(collection, [])], default=0) + 1