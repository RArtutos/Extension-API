"""Authentication configuration module"""
from ...config import Config

class AuthConfig:
    LOGIN_ENDPOINT = '/api/auth/login'
    VALIDATE_ENDPOINT = '/api/auth/validate'
    TOKEN_HEADER = 'Authorization'
    TOKEN_TYPE = 'Bearer'
    API_URL = Config.EXTERNAL_API_URL