from datetime import datetime
from typing import List, Dict, Optional
from ..base import BaseRepository
from ...core.config import settings

class SessionRepository(BaseRepository):
    def create_session(self, session_data: Dict) -> bool:
        data = self._read_data()
        if "sessions" not in data:
            data["sessions"] = []
        
        data["sessions"].append(session_data)
        self._write_data(data)
        return True

    def get_active_sessions(self, user_id: str) -> List[Dict]:
        data = self._read_data()
        timeout = datetime.utcnow() - settings.SESSION_TIMEOUT
        
        return [
            session for session in data.get("sessions", [])
            if session["user_id"] == user_id and
            datetime.fromisoformat(session["last_activity"]) > timeout
        ]

    def update_session_activity(self, session_id: str, activity_data: Dict) -> bool:
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

    def end_session(self, session_id: str) -> bool:
        data = self._read_data()
        session = next(
            (s for s in data.get("sessions", []) if s["id"] == session_id),
            None
        )
        
        if session:
            session["active"] = False
            session["end_time"] = datetime.utcnow().isoformat()
            if session.get("start_time"):
                start = datetime.fromisoformat(session["start_time"])
                end = datetime.utcnow()
                session["duration"] = (end - start).total_seconds()
            
            self._write_data(data)
            return True
        return False