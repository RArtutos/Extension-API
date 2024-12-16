import requests
from typing import List, Dict, Optional
from flask_login import current_user
from ..config import Config

class AccountService:
    def __init__(self):
        self.api_url = f"{Config.API_URL}/api/accounts"
    
    def get_all(self) -> List[Dict]:
        try:
            response = requests.get(
                self.api_url,
                headers={'Authorization': f'Bearer {current_user.token}'}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching accounts: {str(e)}")
            return []
    
    def get_session_info(self, account_id: int) -> Dict:
        try:
            response = requests.get(
                f"{self.api_url}/{account_id}/session",
                headers={'Authorization': f'Bearer {current_user.token}'}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching session info: {str(e)}")
            return {'active_sessions': 0, 'max_concurrent_users': 0}

    def get_analytics(self, account_id: Optional[int] = None) -> List[Dict]:
        try:
            url = f"{Config.API_URL}/api/admin/analytics"
            if account_id:
                url += f"?account_id={account_id}"
            response = requests.get(
                url,
                headers={'Authorization': f'Bearer {current_user.token}'}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching analytics: {str(e)}")
            return []