from flask import session
from typing import Optional, Dict

class SessionManager:
    @staticmethod
    def set_user_session(user_data: Dict) -> None:
        session['user_token'] = user_data['token']
        session['user_email'] = user_data['email']
        session['is_admin'] = user_data['is_admin']
        session.permanent = True

    @staticmethod
    def clear_session() -> None:
        session.clear()

    @staticmethod
    def get_stored_token() -> Optional[str]:
        return session.get('user_token')

    @staticmethod
    def get_user_data() -> Optional[Dict]:
        if 'user_token' not in session:
            return None
        return {
            'token': session['user_token'],
            'email': session['user_email'],
            'is_admin': session['is_admin']
        }