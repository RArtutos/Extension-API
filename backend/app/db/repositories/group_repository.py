from typing import List, Dict, Optional
from ..database import Database

class GroupRepository:
    def __init__(self):
        self.db = Database()

    def get_all(self) -> List[Dict]:
        """Get all groups with their accounts"""
        data = self.db._read_data()
        if "groups" not in data:
            data["groups"] = []
            self.db._write_data(data)
        return data["groups"]

    def create(self, group_data: Dict) -> Optional[Dict]:
        """Create a new group"""
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

    def get_by_id(self, group_id: int) -> Optional[Dict]:
        """Get a group by its ID"""
        data = self.db._read_data()
        return next((g for g in data.get("groups", []) if g["id"] == group_id), None)

    def get_accounts_by_group(self, group_id: int) -> List[Dict]:
        """Get all accounts in a group"""
        data = self.db._read_data()
        return [a for a in data["accounts"] if a.get("group_id") == group_id]

    def assign_account(self, group_id: int, account_id: int) -> bool:
        """Assign an account to a group"""
        data = self.db._read_data()
        
        # Verify group exists
        group = next((g for g in data.get("groups", []) if g["id"] == group_id), None)
        if not group:
            return False
            
        # Verify account exists and update its group
        account = next((a for a in data["accounts"] if a["id"] == account_id), None)
        if not account:
            return False
            
        account["group_id"] = group_id
        self.db._write_data(data)
        return True