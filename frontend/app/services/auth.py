import requests
from ..models.user import User
from ..config import Config

class AuthService:
    def __init__(self):
        self.api_url = f"{Config.API_URL}/api/auth"
    
    def login(self, email: str, password: str) -> User:
        response = requests.post(
            f"{self.api_url}/login",
            data={'username': email, 'password': password}
        )
        if response.status_code == 200:
            data = response.json()
            return User(email=email, token=data['access_token'])
        raise Exception('Invalid credentials')