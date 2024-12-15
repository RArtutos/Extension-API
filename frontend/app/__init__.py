from flask import Flask
from flask_login import LoginManager
from .config import Config
from .models.user import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    # Como estamos usando el email como ID, simplemente devolvemos un nuevo objeto User
    # En una aplicación real, aquí buscaríamos el usuario en la base de datos
    return User(email=user_id, token=None)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    from .routes import auth, accounts, proxies
    app.register_blueprint(auth.bp)
    app.register_blueprint(accounts.bp)
    app.register_blueprint(proxies.bp)
    
    return app