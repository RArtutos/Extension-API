from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .config import Config
from .models.user import User

login_manager = LoginManager()
csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    return User(email=user_id, token=None)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = 'auth.login'
    
    from .routes import auth, accounts, proxies
    app.register_blueprint(auth.bp)
    app.register_blueprint(accounts.bp)
    app.register_blueprint(proxies.bp)
    
    return app