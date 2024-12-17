from typing import Optional, Dict, List
from datetime import datetime
from .repositories.user_repository import UserRepository
from .repositories.account_repository import AccountRepository
from .repositories.user_account_repository import UserAccountRepository
from .repositories.preset_repository import PresetRepository
from .repositories.analytics_repository import AnalyticsRepository
from ..core.config import settings

class Database:
    def __init__(self):
        self.users = UserRepository()
        self.accounts = AccountRepository()
        self.user_accounts = UserAccountRepository()
        self.presets = PresetRepository()
        self.analytics = AnalyticsRepository()

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        return self.users.get_by_email(email)

    def get_users(self):
        return self.users.get_all()

    def get_accounts(self, user_id: Optional[str] = None):
        return self.accounts.get_all(user_id)

    def get_account(self, account_id: int):
        return self.accounts.get_by_id(account_id)

    def get_recent_activities(self, limit: int = 10) -> List[Dict]:
        return self.analytics.get_recent_activities(limit)

    def get_account_sessions(self, account_id: int) -> List[Dict]:
        return self.analytics.get_account_sessions(account_id)

    def get_user_sessions(self, user_id: str) -> List[Dict]:
        return self.analytics.get_user_sessions(user_id)

    def get_account_users(self, account_id: int) -> List[Dict]:
        return self.analytics.get_account_users(account_id)