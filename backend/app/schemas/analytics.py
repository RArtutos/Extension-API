from pydantic import BaseModel
from typing import Optional

class AnalyticsResponse(BaseModel):
    user_id: str
    account_id: int
    domain: str
    action: str
    ip_address: Optional[str]
    timestamp: str