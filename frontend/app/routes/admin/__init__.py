"""Admin routes package initialization"""
from flask import Blueprint

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Import sub-blueprints
from .users import bp as users_bp
from .analytics import bp as analytics_bp
from .presets import bp as presets_bp

# Register sub-blueprints
bp.register_blueprint(users_bp)
bp.register_blueprint(analytics_bp)
bp.register_blueprint(presets_bp)