from flask import session
from typing import Optional
from ..models.user import User

class SessionManager:
    @staticmethod
    def set_user_session(user: User) -> None:
        session['user_token'] = user.token
        session['user_email'] = user.email
        session['is_admin'] = user.is_admin
        session.permanent = True

    @staticmethod
    def clear_session() -> None:
        session.clear()

    @staticmethod
    def get_stored_token() -> Optional[str]:
        return session.get('user_token')