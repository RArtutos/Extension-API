"""Session management service"""
from typing import Dict, Optional
from flask import session
from ...models.user import User

class SessionService:
    @staticmethod
    def set_user_session(user_data: Dict) -> None:
        """Set user session data"""
        session['token'] = user_data.get('token')
        session['user_email'] = user_data.get('email')
        session['is_admin'] = user_data.get('is_admin', False)
        session.permanent = True

    @staticmethod
    def get_stored_token() -> Optional[str]:
        """Get stored authentication token"""
        return session.get('token')

    @staticmethod
    def get_current_user() -> Optional[User]:
        """Get current user from session"""
        if 'user_email' not in session:
            return None
        return User(
            email=session['user_email'],
            is_admin=session.get('is_admin', False)
        )

    @staticmethod
    def clear_session() -> None:
        """Clear all session data"""
        session.clear()