import requests
from typing import Optional
from ..models.user import User
from ..config import Config
from flask import session

class AuthService:
    def __init__(self):
        self.api_url = f"{Config.API_URL}/api/auth"
    
    def login(self, email: str, password: str) -> Optional[User]:
        try:
            response = requests.post(
                f"{self.api_url}/login",
                data={
                    'username': email,
                    'password': password,
                    'grant_type': 'password'
                },
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            )
            
            if response.status_code != 200:
                print(f"Login failed with status {response.status_code}: {response.text}")
                return None
                
            data = response.json()
            user = User(
                email=email,
                token=data['access_token'],
                is_admin=data.get('is_admin', False)
            )
            session['user_token'] = data['access_token']
            return user
        except requests.RequestException as e:
            print(f"Login request failed: {str(e)}")
            return None

    def get_user(self, user_id: str) -> Optional[User]:
        token = session.get('user_token')
        if not token:
            return None

        try:
            response = requests.get(
                f"{Config.API_URL}/api/users/me",
                headers={'Authorization': f'Bearer {token}'}
            )
            
            if response.status_code == 200:
                data = response.json()
                return User(
                    email=data.get('email', user_id),
                    token=token,
                    is_admin=data.get('is_admin', False)
                )
        except:
            pass
        return None