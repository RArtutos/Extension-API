from typing import List, Dict, Optional
from datetime import datetime
from ..database import Database

class GroupRepository:
    def __init__(self):
        self.db = Database()

    def create(self, group_data: Dict) -> Dict:
        data = self.db._read_data()
        if "groups" not in data:
            data["groups"] = []
        
        new_id = max([g.get("id", 0) for g in data["groups"]], default=0) + 1
        
        group = {
            "id": new_id,
            "name": group_data["name"],
            "description": group_data.get("description", ""),
            "created_at": datetime.utcnow().isoformat()
        }
        
        data["groups"].append(group)
        self.db._write_data(data)
        return group

    def get_all(self) -> List[Dict]:
        data = self.db._read_data()
        if "groups" not in data:
            data["groups"] = []
            self.db._write_data(data)
        return data["groups"]

    def get_by_id(self, group_id: int) -> Optional[Dict]:
        data = self.db._read_data()
        return next((g for g in data.get("groups", []) if g["id"] == group_id), None)

    def get_accounts_by_group(self, group_id: int) -> List[Dict]:
        data = self.db._read_data()
        return [a for a in data["accounts"] if a.get("group_id") == group_id]

    def assign_account(self, account_id: int, group_id: int) -> bool:
        data = self.db._read_data()
        account = next((a for a in data["accounts"] if a["id"] == account_id), None)
        group = next((g for g in data.get("groups", []) if g["id"] == group_id), None)
        
        if not account or not group:
            return False
            
        account["group_id"] = group_id
        self.db._write_data(data)
        return True