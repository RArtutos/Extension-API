import requests
from typing import List, Dict
from flask_login import current_user
from ..config import Config

class AdminService:
    def __init__(self):
        self.api_url = f"{Config.API_URL}/api/admin"

    def get_users(self) -> List[Dict]:
        response = requests.get(
            f"{self.api_url}/users",
            headers={'Authorization': f'Bearer {current_user.token}'}
        )
        response.raise_for_status()
        return response.json()

    def create_user(self, data: Dict) -> Dict:
        response = requests.post(
            f"{self.api_url}/users",
            json=data,
            headers={'Authorization': f'Bearer {current_user.token}'}
        )
        response.raise_for_status()
        return response.json()

    def get_analytics(self) -> Dict:
        response = requests.get(
            f"{self.api_url}/analytics",
            headers={'Authorization': f'Bearer {current_user.token}'}
        )
        response.raise_for_status()
        return response.json()

    def assign_account_to_user(self, user_id: str, account_id: int) -> Dict:
        response = requests.post(
            f"{self.api_url}/users/{user_id}/accounts/{account_id}",
            headers={'Authorization': f'Bearer {current_user.token}'}
        )
        response.raise_for_status()
        return response.json()