"""Analytics routes package initialization"""
from flask import Blueprint

bp = Blueprint('analytics', __name__, url_prefix='/analytics')

from . import views  # Import views after blueprint creation to avoid circular imports