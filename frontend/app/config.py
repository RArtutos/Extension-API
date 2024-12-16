import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    API_URL = os.getenv('API_URL', 'http://backend:8000')
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = '/tmp/flask_session'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Ensure the session directory exists
    os.makedirs(SESSION_FILE_DIR, exist_ok=True)