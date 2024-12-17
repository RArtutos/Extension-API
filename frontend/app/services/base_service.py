"""Base service for API interactions"""
from typing import Optional, Dict, Any
import requests
from flask import current_app
from ..core.auth.config import AuthConfig
from ..core.auth.session_service import SessionService
from ..core.auth.token_service import TokenService

class BaseService:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.base_url = AuthConfig.API_URL

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication"""
        token = SessionService.get_stored_token()
        return TokenService.get_headers(token)

    def _handle_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Any:
        """Handle API request with error handling"""
        try:
            url = f"{self.base_url}{endpoint}"
            headers = self._get_headers()
            
            if method == 'get':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'post':
                response = requests.post(url, headers=headers, json=data)
            elif method == 'put':
                response = requests.put(url, headers=headers, json=data)
            elif method == 'delete':
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            # Log request details for debugging
            if current_app:
                current_app.logger.debug(f"Request: {method.upper()} {url}")
                current_app.logger.debug(f"Headers: {headers}")
                if data:
                    current_app.logger.debug(f"Data: {data}")
            
            response.raise_for_status()
            return response.json() if response.content else None
            
        except requests.exceptions.RequestException as e:
            if current_app:
                current_app.logger.error(f"API request failed: {str(e)}")
                if hasattr(e.response, 'text'):
                    current_app.logger.error(f"Response text: {e.response.text}")
            if e.response and e.response.status_code == 401:
                # Clear session on unauthorized
                SessionService.clear_session()
            raise