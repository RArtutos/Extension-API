"""Token management service"""
from typing import Optional, Dict
from .config import AuthConfig
from .exceptions import TokenError

class TokenService:
    @staticmethod
    def format_token(token: str) -> str:
        """Format token for authorization header"""
        return f"{AuthConfig.TOKEN_TYPE} {token}"

    @staticmethod
    def extract_token(header: str) -> Optional[str]:
        """Extract token from authorization header"""
        if not header:
            return None
        parts = header.split()
        if len(parts) != 2 or parts[0] != AuthConfig.TOKEN_TYPE:
            raise TokenError("Invalid token format")
        return parts[1]

    @staticmethod
    def get_headers(token: Optional[str] = None) -> Dict[str, str]:
        """Get request headers with optional token"""
        headers = {'Content-Type': 'application/json'}
        if token:
            headers[AuthConfig.TOKEN_HEADER] = TokenService.format_token(token)
        return headers