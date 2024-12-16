from typing import Optional, Dict
import requests
from flask_login import current_user
from ..core.session import SessionManager
from ..config import Config

class BaseService:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.base_url = Config.API_URL

    def _get_headers(self) -> Dict:
        token = SessionManager.get_stored_token()
        if token:
            return {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        return {'Content-Type': 'application/json'}

    def _handle_request(self, operation: str, endpoint: str, data: Dict = None, params: Dict = None) -> Optional[Dict]:
        try:
            url = f"{self.base_url}{endpoint}"
            headers = self._get_headers()
            
            if operation == 'get':
                response = requests.get(url, headers=headers, params=params)
            elif operation == 'post':
                response = requests.post(url, headers=headers, json=data)
            elif operation == 'put':
                response = requests.put(url, headers=headers, json=data)
            elif operation == 'delete':
                response = requests.delete(url, headers=headers)
            
            response.raise_for_status()
            return response.json() if response.content else None
        except Exception as e:
            print(f"Error in {operation}: {str(e)}")
            return None