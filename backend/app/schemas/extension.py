from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class ExtendedAccount(BaseModel):
    id: int
    name: str
    group: Optional[str] = None
    cookies: List[Dict]
    max_concurrent_users: int
    active_sessions: int
    is_available: bool

class AccountSession(BaseModel):
    account_id: int
    active_sessions: int
    max_concurrent_users: int
    current_user_session: Optional[Dict] = None
    is_available: bool

class SessionCreate(BaseModel):
    device_id: str
    domain: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class SessionUpdate(BaseModel):
    domain: str

class SessionResponse(BaseModel):
    session_id: str
    status: str
    created_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None

class AnalyticsEvent(BaseModel):
    account_id: int
    domain: str
    action: str
    timestamp: datetime
    metadata: Optional[Dict] = None

class BatchAnalyticsEvents(BaseModel):
    events: List[AnalyticsEvent]