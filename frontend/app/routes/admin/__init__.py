"""Admin routes package"""
from flask import Blueprint

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Import views after blueprint creation to avoid circular imports
from . import users, analytics, presets, accounts

# Register routes
bp.add_url_rule('/users', 'list_users', users.list_users)
bp.add_url_rule('/users/create', 'create_user', users.create_user, methods=['GET', 'POST'])
bp.add_url_rule('/users/<user_id>/accounts', 'user_accounts', users.user_accounts)
bp.add_url_rule('/users/<user_id>/accounts/<int:account_id>', 'assign_account', 
                users.assign_account, methods=['POST'])
bp.add_url_rule('/users/<user_id>/accounts/<int:account_id>', 'remove_account', 
                users.remove_account, methods=['DELETE'])

bp.add_url_rule('/analytics', 'analytics_dashboard', analytics.analytics_dashboard)
bp.add_url_rule('/analytics/user/<user_id>', 'user_analytics', analytics.user_analytics)
bp.add_url_rule('/analytics/account/<int:account_id>', 'account_analytics', analytics.account_analytics)

bp.add_url_rule('/presets', 'list_presets', presets.list_presets)
bp.add_url_rule('/presets/create', 'create_preset', presets.create_preset, methods=['GET', 'POST'])
bp.add_url_rule('/presets/<int:preset_id>/edit', 'edit_preset', presets.edit_preset, methods=['GET', 'POST'])
bp.add_url_rule('/presets/<int:preset_id>', 'delete_preset', presets.delete_preset, methods=['DELETE'])