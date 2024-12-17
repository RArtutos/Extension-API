"""Presets routes package initialization"""
from flask import Blueprint

bp = Blueprint('presets', __name__, url_prefix='/presets')

from . import views  # Import views after blueprint creation to avoid circular imports