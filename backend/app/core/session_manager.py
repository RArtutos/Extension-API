from datetime import datetime, timedelta
from typing import Optional, List, Dict
from ..db.database import Database
from ..core.config import settings

class SessionManager:
    def __init__(self):
        self.db = Database()

    def create_session(self, user_id: str, account_id: int, domain: Optional[str] = None) -> bool:
        """Create a new session if limits allow"""
        # Check account limits
        account = self.db.get_account(account_id)
        if not account:
            return False

        active_sessions = self.get_active_sessions(account_id)
        if len(active_sessions) >= account.get('max_concurrent_users', settings.MAX_CONCURRENT_USERS_PER_ACCOUNT):
            return False

        # Create new session
        session = {
            "user_id": user_id,
            "account_id": account_id,
            "domain": domain,
            "last_activity": datetime.utcnow().isoformat()
        }
        
        return self.db.create_session(session)

    def update_session(self, user_id: str, account_id: int, domain: Optional[str] = None) -> bool:
        """Update session last activity"""
        return self.db.update_session_activity(user_id, account_id, domain)

    def cleanup_inactive_sessions(self):
        """Remove inactive sessions based on timeout"""
        timeout = datetime.utcnow() - timedelta(seconds=settings.COOKIE_INACTIVITY_TIMEOUT)
        return self.db.cleanup_inactive_sessions(timeout.isoformat())

    def get_active_sessions(self, account_id: int) -> List[Dict]:
        """Get all active sessions for an account"""
        self.cleanup_inactive_sessions()
        return self.db.get_active_sessions(account_id)

    def remove_session(self, user_id: str, account_id: int) -> bool:
        """Remove a specific session"""
        return self.db.remove_session(user_id, account_id)