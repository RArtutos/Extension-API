"""Users routes package initialization"""
from flask import Blueprint

bp = Blueprint('users', __name__, url_prefix='/users')

from . import views  # Import views after blueprint creation to avoid circular imports