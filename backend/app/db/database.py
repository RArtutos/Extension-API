import json
from typing import Optional, List, Dict
from ..core.config import settings

class Database:
    def __init__(self):
        self.file_path = settings.DATA_FILE

    def _read_data(self) -> dict:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _write_data(self, data: dict):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        data = self._read_data()
        return next((user for user in data["users"] if user["email"] == email), None)

    def create_user(self, email: str, password: str) -> Dict:
        data = self._read_data()
        user = {"email": email, "password": password, "is_admin": False}
        data["users"].append(user)
        self._write_data(data)
        return user

    def get_accounts(self) -> List[Dict]:
        data = self._read_data()
        return data["accounts"]

    def create_account(self, account: Dict) -> Dict:
        data = self._read_data()
        if not data["accounts"]:
            account["id"] = 1
        else:
            account["id"] = max(a["id"] for a in data["accounts"]) + 1
        data["accounts"].append(account)
        self._write_data(data)
        return account

    def delete_account(self, account_id: int) -> bool:
        data = self._read_data()
        initial_length = len(data["accounts"])
        data["accounts"] = [a for a in data["accounts"] if a["id"] != account_id]
        if len(data["accounts"]) != initial_length:
            self._write_data(data)
            return True
        return False

    def get_proxies(self) -> List[Dict]:
        data = self._read_data()
        return data["proxies"]

    def create_proxy(self, proxy: Dict) -> Dict:
        data = self._read_data()
        if not data["proxies"]:
            proxy["id"] = 1
        else:
            proxy["id"] = max(p["id"] for p in data["proxies"]) + 1
        data["proxies"].append(proxy)
        self._write_data(data)
        return proxy

    def delete_proxy(self, proxy_id: int) -> bool:
        data = self._read_data()
        initial_length = len(data["proxies"])
        data["proxies"] = [p for p in data["proxies"] if p["id"] != proxy_id]
        if len(data["proxies"]) != initial_length:
            self._write_data(data)
            return True
        return False