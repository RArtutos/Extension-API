import requests
from typing import List, Dict
from flask_login import current_user
from ..config import Config

class AccountService:
    def __init__(self):
        self.api_url = f"{Config.API_URL}/api/accounts"
    
    def get_all(self) -> List[Dict]:
        response = requests.get(
            self.api_url,
            headers={'Authorization': f'Bearer {current_user.token}'}
        )
        return response.json()
    
    def create(self, data: Dict) -> Dict:
        response = requests.post(
            self.api_url,
            json=data,
            headers={'Authorization': f'Bearer {current_user.token}'}
        )
        return response.json()