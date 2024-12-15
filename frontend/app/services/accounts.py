import requests
from typing import List, Dict
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
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching accounts: {str(e)}")
            return []
    
    def create(self, data: Dict) -> Dict:
        try:
            response = requests.post(
                self.api_url,
                json=data,
                headers={'Authorization': f'Bearer {current_user.token}'}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error creating account: {str(e)}")
            raise Exception(f"Failed to create account: {str(e)}")
    
    def delete(self, account_id: int) -> bool:
        try:
            response = requests.delete(
                f"{self.api_url}/{account_id}",
                headers={'Authorization': f'Bearer {current_user.token}'}
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Error deleting account: {str(e)}")
            return False