"""Authentication exceptions module"""

class AuthenticationError(Exception):
    """Base authentication error"""
    pass

class InvalidCredentialsError(AuthenticationError):
    """Invalid credentials error"""
    pass

class TokenError(AuthenticationError):
    """Token-related error"""
    pass

class ConnectionError(AuthenticationError):
    """Connection error"""
    pass