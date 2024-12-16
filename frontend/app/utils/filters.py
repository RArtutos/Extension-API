from datetime import datetime
from typing import Optional
import pytz

def format_datetime(value: Optional[str]) -> str:
    """Format datetime string to human readable format"""
    if not value:
        return ''
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, AttributeError):
        return str(value)

def timeago(value: Optional[str]) -> str:
    """Convert datetime to relative time string"""
    if not value:
        return ''
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        now = datetime.now(pytz.UTC)
        diff = now - dt

        seconds = diff.total_seconds()
        if seconds < 60:
            return 'just now'
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f'{hours} hour{"s" if hours != 1 else ""} ago'
        elif seconds < 604800:
            days = int(seconds / 86400)
            return f'{days} day{"s" if days != 1 else ""} ago'
        else:
            return format_datetime(value)
    except (ValueError, AttributeError):
        return str(value)