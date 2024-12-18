from datetime import datetime
from typing import List, Dict
from ...db.analytics import AnalyticsDatabase
from ...schemas.analytics import AnalyticsEvent

class EventProcessor:
    def __init__(self):
        self.db = AnalyticsDatabase()

    async def process_events(self, user_id: str, events: List[AnalyticsEvent]):
        """Process a batch of analytics events"""
        for event in events:
            await self.process_event(user_id, event)

    async def process_event(self, user_id: str, event: AnalyticsEvent):
        """Process a single analytics event"""
        if event.type == 'pageview':
            await self.track_page_view(user_id, event.domain, event.account_id)
        elif event.type == 'session':
            await self.track_session_event(user_id, event)
        elif event.type == 'account_switch':
            await self.track_account_switch(user_id, event)

    async def track_page_view(self, user_id: str, domain: str, account_id: int):
        """Track a page view event"""
        self.db.create_analytics_event({
            'user_id': user_id,
            'account_id': account_id,
            'domain': domain,
            'action': 'pageview',
            'timestamp': datetime.utcnow()
        })

    async def track_session_event(self, user_id: str, event: AnalyticsEvent):
        """Track a session event"""
        self.db.create_analytics_event({
            'user_id': user_id,
            'account_id': event.account_id,
            'domain': event.domain,
            'action': event.metadata.get('action', 'unknown'),
            'timestamp': event.timestamp
        })

    async def track_account_switch(self, user_id: str, event: AnalyticsEvent):
        """Track an account switch event"""
        self.db.create_analytics_event({
            'user_id': user_id,
            'account_id': event.account_id,
            'action': 'account_switch',
            'timestamp': event.timestamp,
            'metadata': event.metadata
        })