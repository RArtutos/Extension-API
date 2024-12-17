from typing import Optional, Dict, List
from datetime import datetime
from .repositories.user_repository import UserRepository
from .repositories.account_repository import AccountRepository
from .repositories.user_account_repository import UserAccountRepository
from .repositories.preset_repository import PresetRepository
from ..core.config import settings

class Database:
    def __init__(self):
        self.users = UserRepository()
        self.accounts = AccountRepository()
        self.user_accounts = UserAccountRepository()
        self.presets = PresetRepository()

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        return self.users.get_by_email(email)

    def get_users(self):
        return self.users.get_all()

    def create_user(self, email: str, password: str, is_admin: bool = False, 
                   expires_in_days: Optional[int] = None, preset_id: Optional[int] = None):
        user = self.users.create(email, password, is_admin, expires_in_days, preset_id)
        if user.get("preset_id"):
            preset = self.get_preset(user["preset_id"])
            if preset:
                for account_id in preset["account_ids"]:
                    self.user_accounts.assign_account(user["email"], account_id)
        return user

    def get_accounts(self, user_id: Optional[str] = None):
        return self.accounts.get_all(user_id)

    def get_account(self, account_id: int):
        return self.accounts.get_by_id(account_id)

    def create_account(self, account_data: Dict):
        return self.accounts.create(account_data)

    def update_account(self, account_id: int, account_data: Dict):
        return self.accounts.update(account_id, account_data)

    def delete_account(self, account_id: int):
        return self.accounts.delete(account_id)

    def assign_account_to_user(self, user_id: str, account_id: int):
        return self.user_accounts.assign_account(user_id, account_id)

    def remove_all_user_accounts(self, user_id: str):
        return self.user_accounts.remove_all_user_accounts(user_id)

    # Preset methods
    def get_presets(self) -> List[Dict]:
        return self.presets.get_presets()

    def get_preset(self, preset_id: int) -> Optional[Dict]:
        return self.presets.get_preset(preset_id)

    def create_preset(self, preset_data: Dict) -> Optional[Dict]:
        return self.presets.create_preset(preset_data)

    def update_preset(self, preset_id: int, preset_data: Dict) -> Optional[Dict]:
        return self.presets.update_preset(preset_id, preset_data)

    def delete_preset(self, preset_id: int) -> bool:
        return self.presets.delete_preset(preset_id)

    def get_users_by_preset(self, preset_id: int) -> List[Dict]:
        return self.presets.get_users_by_preset(preset_id)