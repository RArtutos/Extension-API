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

    def get_recent_activities(self, limit: int = 10) -> List[Dict]:
        return self.analytics.get_recent_activities(limit)

    def get_account_sessions(self, account_id: int) -> List[Dict]:
        return self.analytics.get_account_sessions(account_id)

    def get_user_sessions(self, user_id: str) -> List[Dict]:
        return self.analytics.get_user_sessions(user_id)

    def get_account_users(self, account_id: int) -> List[Dict]:
        return self.analytics.get_account_users(account_id)

    def get_user_account_usage(self, user_id: str) -> List[Dict]:
        return self.analytics.get_user_account_usage(user_id)

    def get_user_analytics(self, user_id: str) -> Dict:
        return {
            "user_id": user_id,
            "sessions": self.analytics.get_user_sessions(user_id),
            "account_usage": self.analytics.get_user_account_usage(user_id),
            "total_time": self.analytics.get_user_total_time(user_id),
            "current_sessions": len([s for s in self.analytics.get_user_sessions(user_id) if s.get("active")])
        }