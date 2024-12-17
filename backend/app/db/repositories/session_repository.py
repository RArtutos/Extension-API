from datetime import datetime
from typing import List, Dict, Optional
from ..base import BaseRepository
from ...core.config import settings

class SessionRepository(BaseRepository):
    def __init__(self):
        super().__init__(settings.DATA_FILE)

    def get_active_sessions(self, account_id: int) -> List[Dict]:
        """Get all active sessions for an account"""
        data = self._read_data()
        sessions = data.get("sessions", [])
        
        # Filter active sessions for the specified account
        return [
            session for session in sessions
            if session.get("account_id") == account_id and
            session.get("active", True)
        ]

    def create_session(self, session_data: Dict) -> bool:
        """Create a new session"""
        data = self._read_data()
        if "sessions" not in data:
            data["sessions"] = []
            
        session_id = f"{session_data['user_id']}_{datetime.utcnow().timestamp()}"
        session = {
            "id": session_id,
            "active": True,
            "created_at": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat(),
            **session_data
        }
        
        data["sessions"].append(session)
        self._write_data(data)
        return True

    def update_session_activity(self, session_id: str, activity_data: Dict) -> bool:
        """Update session activity"""
        data = self._read_data()
        session = next(
            (s for s in data.get("sessions", []) if s["id"] == session_id),
            None
        )
        
        if session:
            session.update(activity_data)
            session["last_activity"] = datetime.utcnow().isoformat()
            self._write_data(data)
            return True
        return False

    def remove_session(self, session_id: str) -> bool:
        """Remove a session"""
        data = self._read_data()
        initial_count = len(data.get("sessions", []))
        
        data["sessions"] = [
            s for s in data.get("sessions", [])
            if s["id"] != session_id
        ]
        
        if len(data["sessions"]) < initial_count:
            self._write_data(data)
            return True
        return False