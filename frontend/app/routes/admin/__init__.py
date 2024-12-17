"""Admin routes package"""
from flask import Blueprint

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Import views after blueprint creation to avoid circular imports
from .users import user_views
from .analytics import analytics_views
from .presets import preset_views

# Register routes
bp.add_url_rule('/users', 'list_users', user_views.list_users)
bp.add_url_rule('/users/create', 'create_user', user_views.create_user, methods=['GET', 'POST'])
bp.add_url_rule('/users/<user_id>/accounts', 'user_accounts', user_views.user_accounts)

bp.add_url_rule('/analytics', 'analytics_dashboard', analytics_views.analytics_dashboard)
bp.add_url_rule('/analytics/user/<user_id>', 'user_analytics', analytics_views.user_analytics)
bp.add_url_rule('/analytics/account/<int:account_id>', 'account_analytics', analytics_views.account_analytics)

bp.add_url_rule('/presets', 'list_presets', preset_views.list_presets)
bp.add_url_rule('/presets/create', 'create_preset', preset_views.create_preset, methods=['GET', 'POST'])
bp.add_url_rule('/presets/<int:preset_id>/edit', 'edit_preset', preset_views.edit_preset, methods=['GET', 'POST'])
bp.add_url_rule('/presets/<int:preset_id>', 'delete_preset', preset_views.delete_preset, methods=['DELETE'])