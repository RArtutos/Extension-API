from datetime import datetime, timedelta
from typing import Optional, Dict, List
from .config import settings
from ..db.database import Database

class SessionManager:
    def __init__(self):
        self.db = Database()

    async def create_session(self, user_id: str, device_info: Dict) -> Optional[str]:
        """Crear nueva sesión si no se excede el límite de dispositivos"""
        user = self.db.get_user_by_email(user_id)
        if not user:
            return None

        active_sessions = self.db.get_active_sessions(user_id)
        if len(active_sessions) >= user.get('max_devices', 1):
            return None

        session_id = f"{user_id}_{datetime.utcnow().timestamp()}"
        session_data = {
            "id": session_id,
            "user_id": user_id,
            "device_id": device_info.get("device_id"),
            "ip_address": device_info.get("ip_address"),
            "user_agent": device_info.get("user_agent"),
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow()
        }

        if self.db.create_session(session_data):
            return session_id
        return None

    def update_session(self, account_id: int, session_data: Dict) -> bool:
        """Update session status for an account"""
        try:
            # Get current session info
            active_sessions = self.get_active_sessions(account_id)
            max_users = self.get_max_concurrent_users(account_id)

            if active_sessions >= max_users and session_data.get('active', True):
                return False

            # Update session
            return self.db.update_session_activity(account_id, session_data)
        except Exception as e:
            print(f"Error in session manager: {str(e)}")
            return False

    def get_user_sessions(self, user_id: str) -> List[Dict]:
        """Obtener sesiones activas del usuario"""
        return self.db.get_active_sessions(user_id)

    def validate_session(self, session_id: str) -> bool:
        """Validar si una sesión está activa y no ha expirado"""
        session = self.db.get_session(session_id)
        if not session:
            return False

        timeout = datetime.utcnow() - timedelta(minutes=settings.SESSION_TIMEOUT_MINUTES)
        return datetime.fromisoformat(session["last_activity"]) > timeout

    def end_session(self, session_id: str) -> bool:
        """Finalizar una sesión"""
        return self.db.remove_session(session_id)


    def get_active_sessions(self, account_id: int) -> int:
        """Get number of active sessions for an account"""
        try:
            sessions = self.db.sessions.get_active_sessions(account_id)
            return len(sessions)
        except Exception:
            return 0


    def get_max_concurrent_users(self, account_id: int) -> int:
        """Get maximum concurrent users allowed for an account"""
        try:
            account = self.db.get_account(account_id)
            return account.get('max_concurrent_users', 1)
        except Exception:
            return 1

    def get_session_info(self, account_id: int) -> Dict:
        """Get session information for an account"""
        active_sessions = self.get_active_sessions(account_id)
        max_users = self.get_max_concurrent_users(account_id)
        
        return {
            'active_sessions': active_sessions,
            'max_concurrent_users': max_users
        }
