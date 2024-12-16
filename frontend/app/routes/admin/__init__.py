from flask import Blueprint
from flask_login import login_required
from ...core.auth import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Import views after blueprint creation to avoid circular imports
from . import users, analytics, presets

# Register presets routes
bp.add_url_rule('/presets', 'list_presets', 
                view_func=login_required(admin_required(presets.list_presets)))
bp.add_url_rule('/presets/create', 'create_preset',
                view_func=login_required(admin_required(presets.create_preset)),
                methods=['GET', 'POST'])
bp.add_url_rule('/presets/<int:preset_id>/edit', 'edit_preset',
                view_func=login_required(admin_required(presets.edit_preset)),
                methods=['GET', 'POST'])
bp.add_url_rule('/presets/<int:preset_id>/delete', 'delete_preset',
                view_func=login_required(admin_required(presets.delete_preset)),
                methods=['POST'])