"""Template filters for the application"""
from datetime import datetime
from typing import Optional

def format_datetime(value: Optional[datetime | str]) -> str:
    """Format datetime for display"""
    if not value:
        return "Never"
    
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            return value
            
    return value.strftime("%Y-%m-%d %H:%M:%S")

def register_filters(app):
    """Register all template filters"""
    app.jinja_env.filters['datetime'] = format_datetime