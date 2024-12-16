from typing import List, Dict, Optional
from datetime import datetime
from .base_repository import BaseRepository

class AccountRepository(BaseRepository):
    def get_all(self, user_email: Optional[str] = None) -> List[Dict]:
        """Get all accounts, optionally filtered by user email"""
        data = self._read_data()
        accounts = data.get("accounts", [])
        groups = {g["id"]: g["name"] for g in data.get("groups", [])}

        # If user email is provided and user is not admin, filter accounts
        if user_email:
            user = next((u for u in data["users"] if u["email"] == user_email), None)
            if user and not user.get("is_admin"):
                user_accounts = [ua["account_id"] for ua in data["user_accounts"] 
                               if ua["user_id"] == user_email]
                accounts = [a for a in accounts if a["id"] in user_accounts]

        # Enrich accounts with additional information
        for account in accounts:
            self._enrich_account(account, data, groups)

        return accounts

    def _enrich_account(self, account: Dict, data: Dict, groups: Dict) -> Dict:
        """Enrich account with additional information like sessions and group name"""
        # Add group information
        if account.get("group_id") and account["group_id"] in groups:
            account["group"] = groups[account["group_id"]]
        else:
            account["group"] = None

        # Add session information
        account_sessions = [
            ua for ua in data["user_accounts"]
            if ua["account_id"] == account["id"] and ua["active_sessions"] > 0
        ]

        account["active_sessions"] = sum(ua["active_sessions"] for ua in account_sessions)
        account["active_users"] = [
            {
                "user_id": ua["user_id"],
                "sessions": ua["active_sessions"],
                "last_activity": ua["last_activity"]
            }
            for ua in account_sessions
        ]

        return account

    def create(self, account_data: Dict) -> Optional[Dict]:
        """Create a new account"""
        try:
            data = self._read_data()
            
            # Validate required fields
            if not account_data.get("name"):
                raise ValueError("Account name is required")

            account_id = self._get_next_id("accounts")
            account = {
                "id": account_id,
                "name": account_data["name"],
                "group_id": account_data.get("group"),
                "cookies": account_data.get("cookies", []),
                "max_concurrent_users": account_data.get("max_concurrent_users", 1),
                "created_at": datetime.utcnow().isoformat()
            }
            
            data["accounts"].append(account)
            self._write_data(data)

            # Enrich and return the created account
            groups = {g["id"]: g["name"] for g in data.get("groups", [])}
            return self._enrich_account(account.copy(), data, groups)
        except Exception as e:
            print(f"Error creating account: {str(e)}")
            return None

    def get_by_id(self, account_id: int) -> Optional[Dict]:
        """Get account by ID"""
        data = self._read_data()
        account = next((a for a in data.get("accounts", []) if a["id"] == account_id), None)
        if account:
            groups = {g["id"]: g["name"] for g in data.get("groups", [])}
            return self._enrich_account(account.copy(), data, groups)
        return None

    def update(self, account_id: int, account_data: Dict) -> Optional[Dict]:
        """Update an existing account"""
        try:
            data = self._read_data()
            account = next((a for a in data["accounts"] if a["id"] == account_id), None)
            
            if not account:
                return None
                
            # Update account fields
            account.update({
                "name": account_data["name"],
                "group_id": account_data.get("group"),
                "cookies": account_data.get("cookies", []),
                "max_concurrent_users": account_data.get("max_concurrent_users", 1)
            })
            
            self._write_data(data)
            
            # Enrich and return the updated account
            groups = {g["id"]: g["name"] for g in data.get("groups", [])}
            return self._enrich_account(account.copy(), data, groups)
        except Exception as e:
            print(f"Error updating account: {str(e)}")
            return None

    def get_status(self, account_id: int) -> Optional[Dict]:
        """Get account status including sessions and active users"""
        data = self._read_data()
        account = next((a for a in data["accounts"] if a["id"] == account_id), None)
        
        if not account:
            return None
            
        account_sessions = [
            ua for ua in data["user_accounts"]
            if ua["account_id"] == account_id and ua["active_sessions"] > 0
        ]
        
        return {
            "id": account_id,
            "active_sessions": sum(ua["active_sessions"] for ua in account_sessions),
            "max_concurrent_users": account.get("max_concurrent_users", 1),
            "active_users": [
                {
                    "user_id": ua["user_id"],
                    "sessions": ua["active_sessions"],
                    "last_activity": ua["last_activity"]
                }
                for ua in account_sessions
            ]
        }