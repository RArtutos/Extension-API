from typing import List, Dict, Optional
from datetime import datetime
from ..database import Database

class AccountRepository:
    def __init__(self):
        self.db = Database()

    def create(self, account_data: Dict) -> Optional[Dict]:
        data = self.db._read_data()
        
        new_id = max([a.get("id", 0) for a in data["accounts"]], default=0) + 1
        
        account = {
            "id": new_id,
            "name": account_data["name"],
            "group_id": int(account_data["group"]) if account_data.get("group") else None,
            "cookies": account_data.get("cookies", []),
            "max_concurrent_users": account_data.get("max_concurrent_users", 1),  # Default to 1
            "active_sessions": 0,
            "active_users": []
        }
        
        data["accounts"].append(account)
        self.db._write_data(data)
        return self._enrich_account(account, data)

    def get_all(self, user_email: Optional[str] = None) -> List[Dict]:
        self.db._cleanup_inactive_sessions()
        data = self.db._read_data()
        accounts = data["accounts"]
        groups = {g["id"]: g["name"] for g in data.get("groups", [])}
        
        if user_email:
            user = self.db.get_user_by_email(user_email)
            if not user.get("is_admin"):
                user_accounts = [ua["account_id"] for ua in data["user_accounts"] 
                               if ua["user_id"] == user_email]
                accounts = [a for a in accounts if a["id"] in user_accounts]
        
        return [self._enrich_account(account, data, groups) for account in accounts]

    def _enrich_account(self, account: Dict, data: Dict, groups: Optional[Dict] = None) -> Dict:
        if groups is None:
            groups = {g["id"]: g["name"] for g in data.get("groups", [])}

        account_sessions = [
            ua for ua in data["user_accounts"]
            if ua["account_id"] == account["id"] and ua["active_sessions"] > 0
        ]
        
        enriched = {
            **account,
            "active_sessions": sum(ua["active_sessions"] for ua in account_sessions),
            "active_users": [
                {
                    "user_id": ua["user_id"],
                    "sessions": ua["active_sessions"],
                    "last_activity": ua["last_activity"]
                }
                for ua in account_sessions
            ]
        }

        # Add group name if account has a group_id
        if account.get("group_id") and account["group_id"] in groups:
            enriched["group"] = groups[account["group_id"]]
        else:
            enriched["group"] = None

        return enriched

    def update(self, account_id: int, account_data: Dict) -> Optional[Dict]:
        data = self.db._read_data()
        account = next((a for a in data["accounts"] if a["id"] == account_id), None)
        
        if not account:
            return None
            
        account.update({
            "name": account_data["name"],
            "group_id": int(account_data["group"]) if account_data.get("group") else None,
            "cookies": account_data.get("cookies", []),
            "max_concurrent_users": account_data.get("max_concurrent_users", 1)  # Default to 1
        })
        
        self.db._write_data(data)
        return self._enrich_account(account, data)