from flask import Blueprint
from flask_login import login_required
from ...core.auth.decorators import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Import views after blueprint creation to avoid circular imports
from . import users, analytics, presets

# Register routes from the view modules
bp.add_url_rule('/users', 'list_users', 
                view_func=login_required(admin_required(users.user_views.list_users)))
bp.add_url_rule('/users/create', 'create_user',
                view_func=login_required(admin_required(users.user_views.create_user)),
                methods=['GET', 'POST'])
bp.add_url_rule('/users/<user_id>/accounts', 'user_accounts',
                view_func=login_required(admin_required(users.user_views.user_accounts)))

bp.add_url_rule('/analytics', 'analytics_dashboard',
                view_func=login_required(admin_required(analytics.analytics_views.analytics_dashboard)))
bp.add_url_rule('/analytics/user/<user_id>', 'user_analytics',
                view_func=login_required(admin_required(analytics.analytics_views.user_analytics)))
bp.add_url_rule('/analytics/account/<int:account_id>', 'account_analytics',
                view_func=login_required(admin_required(analytics.analytics_views.account_analytics)))

bp.add_url_rule('/presets', 'list_presets',
                view_func=login_required(admin_required(presets.preset_views.list_presets)))
bp.add_url_rule('/presets/create', 'create_preset',
                view_func=login_required(admin_required(presets.preset_views.create_preset)),
                methods=['GET', 'POST'])
bp.add_url_rule('/presets/<int:preset_id>/edit', 'edit_preset',
                view_func=login_required(admin_required(presets.preset_views.edit_preset)),
                methods=['GET', 'POST'])
bp.add_url_rule('/presets/<int:preset_id>', 'delete_preset',
                view_func=login_required(admin_required(presets.preset_views.delete_preset)),
                methods=['DELETE'])