from datetime import datetime, timedelta
from typing import Optional, Dict, List
from .config import settings
from ..db.database import Database

class SessionManager:
    def __init__(self):
        self.db = Database()

    def get_session_info(self, account_id: int) -> Dict:
        """Get session information for an account"""
        try:
            active_sessions = self.db.get_active_sessions(account_id)
            account = self.db.get_account(account_id)
            max_users = account.get('max_concurrent_users', 1) if account else 1
            
            return {
                'active_sessions': len(active_sessions),
                'max_concurrent_users': max_users
            }
        except Exception as e:
            print(f"Error getting session info: {str(e)}")
            return {
                'active_sessions': 0,
                'max_concurrent_users': 1
            }

    def update_session(self, account_id: int, session_data: Dict) -> bool:
        """Update session status for an account"""
        try:
            # Verificar límites de sesión
            session_info = self.get_session_info(account_id)
            if not session_data.get('active', True):
                # Si estamos terminando la sesión, siempre permitir
                return self.db.update_session_activity(account_id, session_data)
                
            if session_info['active_sessions'] >= session_info['max_concurrent_users']:
                return False

            # Actualizar la sesión
            session_data['last_activity'] = datetime.utcnow().isoformat()
            return self.db.update_session_activity(account_id, session_data)
        except Exception as e:
            print(f"Error updating session: {str(e)}")
            return False

    def start_session(self, account_id: int, user_id: str, domain: str) -> bool:
        """Start a new session"""
        try:
            session_info = self.get_session_info(account_id)
            if session_info['active_sessions'] >= session_info['max_concurrent_users']:
                return False

            session_data = {
                'account_id': account_id,
                'user_id': user_id,
                'domain': domain,
                'active': True,
                'created_at': datetime.utcnow().isoformat(),
                'last_activity': datetime.utcnow().isoformat()
            }

            return self.db.create_session(session_data)
        except Exception as e:
            print(f"Error starting session: {str(e)}")
            return False

    def end_session(self, account_id: int, user_id: str) -> bool:
        """End a session"""
        try:
            session_data = {
                'active': False,
                'end_time': datetime.utcnow().isoformat()
            }
            return self.db.update_session_activity(account_id, session_data)
        except Exception as e:
            print(f"Error ending session: {str(e)}")
            return False