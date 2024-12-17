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
bp.add_url_rule('/analytics', 'admin_analytics_dashboard',
                view_func=login_required(admin_required(analytics_views.analytics_dashboard)))
bp.add_url_rule('/analytics/user/<user_id>', 'admin_user_analytics',
                view_func=login_required(admin_required(analytics_views.user_analytics)))
bp.add_url_rule('/analytics/account/<int:account_id>', 'admin_account_analytics',
                view_func=login_required(admin_required(analytics_views.account_analytics)))

# User management routes
bp.add_url_rule('/users', 'admin_list_users',
                view_func=login_required(admin_required(user_views.list_users)))
bp.add_url_rule('/users/create', 'admin_create_user',
                view_func=login_required(admin_required(user_views.create_user)),
                methods=['GET', 'POST'])
bp.add_url_rule('/users/<user_id>/accounts', 'admin_user_accounts',
                view_func=login_required(admin_required(user_views.user_accounts)))

# Preset management routes
bp.add_url_rule('/presets', 'admin_list_presets',
                view_func=login_required(admin_required(preset_views.list_presets)))
bp.add_url_rule('/presets/create', 'admin_create_preset',
                view_func=login_required(admin_required(preset_views.create_preset)),
                methods=['GET', 'POST'])