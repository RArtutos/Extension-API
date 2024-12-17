from flask import Blueprint
from flask_login import login_required
from ...core.auth import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Import views
from .users import user_views
from .presets import preset_views
from .analytics import analytics_views

# Register view functions
# Analytics routes
bp.add_url_rule('/analytics', 'analytics_dashboard',
                view_func=login_required(admin_required(analytics_views.analytics_dashboard)))
bp.add_url_rule('/analytics/user/<user_id>', 'user_analytics',
                view_func=login_required(admin_required(analytics_views.user_analytics)))
bp.add_url_rule('/analytics/account/<int:account_id>', 'account_analytics',
                view_func=login_required(admin_required(analytics_views.account_analytics)))

# User management routes
bp.add_url_rule('/users', 'list_users',
                view_func=login_required(admin_required(user_views.list_users)))
bp.add_url_rule('/users/create', 'create_user',
                view_func=login_required(admin_required(user_views.create_user)),
                methods=['GET', 'POST'])
bp.add_url_rule('/users/<user_id>/accounts', 'user_accounts',
                view_func=login_required(admin_required(user_views.user_accounts)))

# Preset management routes
bp.add_url_rule('/presets', 'list_presets',
                view_func=login_required(admin_required(preset_views.list_presets)))
bp.add_url_rule('/presets/create', 'create_preset',
                view_func=login_required(admin_required(preset_views.create_preset)),
                methods=['GET', 'POST'])
bp.add_url_rule('/presets/<int:preset_id>/edit', 'edit_preset',
                view_func=login_required(admin_required(preset_views.edit_preset)),
                methods=['GET', 'POST'])