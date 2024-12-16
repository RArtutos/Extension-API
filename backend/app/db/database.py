import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from ..core.config import settings
from ..core.auth import get_password_hash

class Database:
    def __init__(self):
        self.file_path = settings.DATA_FILE

    def _read_data(self) -> dict:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _write_data(self, data: dict):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)

    # User methods
    def get_users(self) -> List[Dict]:
        data = self._read_data()
        users = data.get("users", [])
        # Add assigned accounts to each user
        for user in users:
            user["assigned_accounts"] = [
                ua["account_id"] for ua in data.get("user_accounts", [])
                if ua["user_id"] == user["email"]
            ]
        return users

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        data = self._read_data()
        user = next((user for user in data["users"] if user["email"] == email), None)
        
        if user:
            # Check expiration
            if user.get("expires_at"):
                expires_at = datetime.fromisoformat(user["expires_at"])
                if datetime.utcnow() > expires_at:
                    return None
                    
            # Add assigned accounts
            user["assigned_accounts"] = [
                ua["account_id"] for ua in data["user_accounts"] 
                if ua["user_id"] == email
            ]
        return user

    def create_user(self, email: str, password: str, is_admin: bool = False, 
                   expires_in_days: Optional[int] = None, preset_id: Optional[int] = None) -> Dict:
        data = self._read_data()
        
        expires_at = None
        if expires_in_days is not None:
            expires_at = (datetime.utcnow() + timedelta(days=expires_in_days)).isoformat()

        user = {
            "email": email,
            "password": get_password_hash(password),
            "is_admin": is_admin,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": expires_at,
            "preset_id": preset_id,
            "assigned_accounts": []
        }
        
        data["users"].append(user)
        self._write_data(data)

        # Apply preset if provided
        if preset_id is not None:
            preset = self.get_preset(preset_id)
            if preset:
                for account_id in preset["account_ids"]:
                    self.assign_account_to_user(email, account_id)

        return user

    # Account methods
    def get_accounts(self, user_id: str = None) -> List[Dict]:
        data = self._read_data()
        if user_id:
            user_account_ids = [ua["account_id"] for ua in data.get("user_accounts", []) 
                              if ua["user_id"] == user_id]
            return [acc for acc in data.get("accounts", []) if acc["id"] in user_account_ids]
        return data.get("accounts", [])

    def create_account(self, account_data: Dict) -> Dict:
        data = self._read_data()
        if "accounts" not in data:
            data["accounts"] = []
            
        account_id = max([a.get("id", 0) for a in data["accounts"]], default=0) + 1
        account = {
            "id": account_id,
            **account_data
        }
        
        data["accounts"].append(account)
        self._write_data(data)
        return account

    def get_account(self, account_id: int) -> Optional[Dict]:
        data = self._read_data()
        return next(
            (acc for acc in data.get("accounts", []) if acc["id"] == account_id),
            None
        )

    def update_account(self, account_id: int, account_data: Dict) -> Optional[Dict]:
        data = self._read_data()
        account_index = next(
            (i for i, a in enumerate(data.get("accounts", []))
             if a["id"] == account_id),
            None
        )
        
        if account_index is not None:
            account = data["accounts"][account_index]
            account.update(account_data)
            self._write_data(data)
            return account
        return None

    def delete_account(self, account_id: int) -> bool:
        data = self._read_data()
        initial_count = len(data.get("accounts", []))
        
        data["accounts"] = [
            a for a in data.get("accounts", [])
            if a["id"] != account_id
        ]
        
        # Also remove account assignments
        data["user_accounts"] = [
            ua for ua in data.get("user_accounts", [])
            if ua["account_id"] != account_id
        ]
        
        if len(data["accounts"]) < initial_count:
            self._write_data(data)
            return True
        return False

    # User-Account relationship methods
    def assign_account_to_user(self, user_id: str, account_id: int) -> bool:
        data = self._read_data()
        
        # Check if user and account exist
        user = self.get_user_by_email(user_id)
        account = self.get_account(account_id)
        if not user or not account:
            return False
            
        # Check if assignment already exists
        if any(ua["user_id"] == user_id and ua["account_id"] == account_id 
               for ua in data.get("user_accounts", [])):
            return False
            
        if "user_accounts" not in data:
            data["user_accounts"] = []
            
        assignment = {
            "user_id": user_id,
            "account_id": account_id,
            "assigned_at": datetime.utcnow().isoformat()
        }
        
        data["user_accounts"].append(assignment)
        self._write_data(data)
        return True

    def remove_account_from_user(self, user_id: str, account_id: int) -> bool:
        data = self._read_data()
        initial_count = len(data.get("user_accounts", []))
        
        data["user_accounts"] = [
            ua for ua in data.get("user_accounts", [])
            if not (ua["user_id"] == user_id and ua["account_id"] == account_id)
        ]
        
        if len(data["user_accounts"]) < initial_count:
            self._write_data(data)
            return True
        return False

    # Session management methods
    def create_session(self, session_data: Dict) -> bool:
        data = self._read_data()
        if "sessions" not in data:
            data["sessions"] = []
            
        session_id = max([s.get("id", 0) for s in data["sessions"]], default=0) + 1
        session = {
            "id": session_id,
            **session_data
        }
        
        data["sessions"].append(session)
        self._write_data(data)
        return True

    def update_session_activity(self, user_id: str, account_id: int, domain: Optional[str] = None) -> bool:
        data = self._read_data()
        session = next(
            (s for s in data.get("sessions", []) 
             if s["user_id"] == user_id and s["account_id"] == account_id),
            None
        )
        
        if session:
            session["last_activity"] = datetime.utcnow().isoformat()
            session["domain"] = domain
            self._write_data(data)
            return True
        return False

    def cleanup_inactive_sessions(self, timeout_timestamp: str) -> int:
        data = self._read_data()
        initial_count = len(data.get("sessions", []))
        
        data["sessions"] = [
            s for s in data.get("sessions", [])
            if s["last_activity"] > timeout_timestamp
        ]
        
        self._write_data(data)
        return initial_count - len(data["sessions"])

    def get_active_sessions(self, account_id: int) -> List[Dict]:
        data = self._read_data()
        return [s for s in data.get("sessions", []) if s["account_id"] == account_id]

    def remove_session(self, user_id: str, account_id: int) -> bool:
        data = self._read_data()
        initial_count = len(data.get("sessions", []))
        
        data["sessions"] = [
            s for s in data.get("sessions", [])
            if not (s["user_id"] == user_id and s["account_id"] == account_id)
        ]
        
        if len(data["sessions"]) < initial_count:
            self._write_data(data)
            return True
        return False

    # Preset methods
    def get_preset(self, preset_id: int) -> Optional[Dict]:
        data = self._read_data()
        return next(
            (p for p in data.get("presets", []) if p["id"] == preset_id),
            None
        )

    def get_presets(self) -> List[Dict]:
        data = self._read_data()
        return data.get("presets", [])