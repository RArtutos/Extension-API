from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel

class AccessLog(BaseModel):
    user_id: str
    account_id: int
    domain: str
    timestamp: datetime
    action: str  # 'login', 'logout', 'access'
    ip_address: Optional[str] = None

class AccountActivity(BaseModel):
    account_id: int
    user_id: str
    action: str
    timestamp: datetime
    ip_address: Optional[str]
    user_agent: Optional[str]
    domain: Optional[str]

class DomainUsage(BaseModel):
    domain: str
    total_time: int
    total_sessions: int

class UserAnalytics(BaseModel):
    user_id: str
    total_time: int
    total_sessions: int
    current_sessions: int
    last_activity: Optional[datetime]
    account_usage: List[Dict]

class AccountAnalytics(BaseModel):
    account_id: int
    total_users: int
    active_users: int
    total_sessions: int
    current_sessions: int
    usage_by_domain: List[DomainUsage]
    user_activities: List[AccountActivity]

class AnalyticsEvent(BaseModel):
    type: str  # 'pageview', 'session', 'account_switch'
    account_id: int
    domain: str
    timestamp: datetime = datetime.utcnow()
    metadata: Optional[Dict] = None

class BatchAnalyticsEvents(BaseModel):
    user_id: str
    events: List[AnalyticsEvent]