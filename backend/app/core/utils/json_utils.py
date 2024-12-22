from datetime import datetime
from pydantic import HttpUrl
import json

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles datetime objects and Pydantic URLs"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, HttpUrl):
            return str(obj)  # Convert HttpUrl to string
        return super().default(obj)

def serialize_datetime(obj):
    """Convert datetime objects to ISO format strings"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, HttpUrl):
        return str(obj)  # Convert HttpUrl to string
    return obj
