from typing import Optional, Dict
from ..core.http_client import HttpClient
from ..config import Config

class BaseService:
    def __init__(self, endpoint: str):
        self.http_client = HttpClient(Config.API_URL)
        self.endpoint = endpoint

    def _handle_request(self, operation: str, *args, **kwargs) -> Optional[Dict]:
        try:
            return getattr(self.http_client, operation)(*args, **kwargs)
        except Exception as e:
            print(f"Error in {operation}: {str(e)}")
            return None