from typing import List, Dict, Optional
from datetime import datetime
from .base_repository import BaseRepository

class GroupRepository(BaseRepository):
    def get_all(self) -> List[Dict]:
        data = self._read_data()
        if "groups" not in data:
            data["groups"] = []
            self._write_data(data)
        return data["groups"]

    def create(self, group_data: Dict) -> Optional[Dict]:
        data = self._read_data()
        if "groups" not in data:
            data["groups"] = []

        group_id = self._get_next_id("groups")
        group = {
            "id": group_id,
            "name": group_data["name"],
            "description": group_data.get("description", ""),
            "created_at": datetime.utcnow().isoformat()
        }
        
        data["groups"].append(group)
        self._write_data(data)
        return group

    def get_by_id(self, group_id: int) -> Optional[Dict]:
        data = self._read_data()
        return next((g for g in data.get("groups", []) if g["id"] == group_id), None)

    def get_accounts_by_group(self, group_id: int) -> List[Dict]:
        data = self._read_data()
        return [a for a in data["accounts"] if a.get("group_id") == group_id]

    def assign_account(self, group_id: int, account_id: int) -> bool:
        data = self._read_data()
        
        group = next((g for g in data.get("groups", []) if g["id"] == group_id), None)
        if not group:
            return False
            
        account = next((a for a in data["accounts"] if a["id"] == account_id), None)
        if not account:
            return False
            
        account["group_id"] = group_id
        self._write_data(data)
        return True