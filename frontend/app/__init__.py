from flask import Flask, session
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from .config import Config
from .models.user import User

login_manager = LoginManager()
csrf = CSRFProtect()
flask_session = Session()

@login_manager.user_loader
def load_user(user_id):
    if 'user_token' not in session:
        return None
    
    from .services.auth import AuthService
    auth_service = AuthService()
    return auth_service.get_user(user_id)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    login_manager.init_app(app)
    csrf.init_app(app)
    flask_session.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    from .routes import auth, accounts, proxies, admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(accounts.bp)
    app.register_blueprint(proxies.bp)
    app.register_blueprint(admin.bp)
    
    return app