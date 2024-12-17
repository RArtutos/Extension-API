"""Database module for handling all database operations"""
from typing import Optional, Dict, List
from datetime import datetime
from .repositories.user_repository import UserRepository
from .repositories.account_repository import AccountRepository
from .repositories.user_account_repository import UserAccountRepository
from .repositories.preset_repository import PresetRepository
from .repositories.analytics_repository import AnalyticsRepository
from .repositories.session_repository import SessionRepository

class Database:
    def __init__(self):
        self.users = UserRepository()
        self.accounts = AccountRepository()
        self.user_accounts = UserAccountRepository()
        self.presets = PresetRepository()
        self.analytics = AnalyticsRepository()
        self.sessions = SessionRepository()

    # User methods
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        return self.users.get_by_email(email)

    def get_users(self) -> List[Dict]:
        return self.users.get_all()

    def create_user(self, user_data: Dict) -> Optional[Dict]:
        return self.users.create(user_data)

    # Account methods
    def get_accounts(self, user_id: Optional[str] = None) -> List[Dict]:
        return self.accounts.get_all(user_id)

    def get_account(self, account_id: int) -> Optional[Dict]:
        return self.accounts.get_by_id(account_id)

    def create_account(self, account_data: Dict) -> Optional[Dict]:
        return self.accounts.create(account_data)

    def update_account(self, account_id: int, account_data: Dict) -> Optional[Dict]:
        return self.accounts.update(account_id, account_data)

    def delete_account(self, account_id: int) -> bool:
        return self.accounts.delete(account_id)

    # User-Account methods
    def assign_account_to_user(self, user_id: str, account_id: int) -> bool:
        return self.user_accounts.assign_account(user_id, account_id)

    def remove_account_from_user(self, user_id: str, account_id: int) -> bool:
        return self.user_accounts.remove_account(user_id, account_id)

    def get_user_accounts(self, user_id: str) -> List[int]:
        return self.user_accounts.get_user_accounts(user_id)

    # Session methods
    def get_active_sessions(self, user_id: str) -> List[Dict]:
        return self.sessions.get_active_sessions(user_id)

    def create_session(self, session_data: Dict) -> bool:
        return self.sessions.create_session(session_data)

    def update_session_activity(self, session_id: str, activity_data: Dict) -> bool:
        return self.sessions.update_session_activity(session_id, activity_data)

    def end_session(self, session_id: str) -> bool:
        return self.sessions.end_session(session_id)

    def get_session(self, session_id: str) -> Optional[Dict]:
        return self.sessions.get_session(session_id)

    # Preset methods
    def get_presets(self) -> List[Dict]:
        return self.presets.get_all()

    def get_preset(self, preset_id: int) -> Optional[Dict]:
        return self.presets.get_by_id(preset_id)

    def create_preset(self, preset_data: Dict) -> Optional[Dict]:
        return self.presets.create_preset(preset_data)

    def update_preset(self, preset_id: int, preset_data: Dict) -> Optional[Dict]:
        return self.presets.update_preset(preset_id, preset_data)

    def delete_preset(self, preset_id: int) -> bool:
        return self.presets.delete_preset(preset_id)