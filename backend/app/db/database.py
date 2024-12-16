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

    # User methods with expiration support
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
            (s for s in data["sessions"] 
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
        initial_count = len(data["sessions"])
        
        data["sessions"] = [
            s for s in data["sessions"]
            if s["last_activity"] > timeout_timestamp
        ]
        
        self._write_data(data)
        return initial_count - len(data["sessions"])

    def get_active_sessions(self, account_id: int) -> List[Dict]:
        data = self._read_data()
        return [s for s in data["sessions"] if s["account_id"] == account_id]

    def remove_session(self, user_id: str, account_id: int) -> bool:
        data = self._read_data()
        initial_count = len(data["sessions"])
        
        data["sessions"] = [
            s for s in data["sessions"]
            if not (s["user_id"] == user_id and s["account_id"] == account_id)
        ]
        
        if len(data["sessions"]) < initial_count:
            self._write_data(data)
            return True
        return False

    # Preset management methods
    def create_preset(self, preset_data: Dict) -> Dict:
        data = self._read_data()
        if "presets" not in data:
            data["presets"] = []
            
        preset_id = max([p.get("id", 0) for p in data["presets"]], default=0) + 1
        preset = {
            "id": preset_id,
            "created_at": datetime.utcnow().isoformat(),
            **preset_data
        }
        
        data["presets"].append(preset)
        self._write_data(data)
        return preset

    def get_preset(self, preset_id: int) -> Optional[Dict]:
        data = self._read_data()
        return next(
            (p for p in data.get("presets", []) if p["id"] == preset_id),
            None
        )

    def get_presets(self) -> List[Dict]:
        data = self._read_data()
        return data.get("presets", [])

    def update_preset(self, preset_id: int, preset_data: Dict) -> Optional[Dict]:
        data = self._read_data()
        preset_index = next(
            (i for i, p in enumerate(data.get("presets", []))
             if p["id"] == preset_id),
            None
        )
        
        if preset_index is not None:
            preset = data["presets"][preset_index]
            preset.update(preset_data)
            self._write_data(data)
            return preset
        return None

    def delete_preset(self, preset_id: int) -> bool:
        data = self._read_data()
        initial_count = len(data.get("presets", []))
        
        data["presets"] = [
            p for p in data.get("presets", [])
            if p["id"] != preset_id
        ]
        
        if len(data["presets"]) < initial_count:
            self._write_data(data)
            return True
        return False