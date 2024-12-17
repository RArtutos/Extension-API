"""Admin routes blueprint configuration"""
from flask import Blueprint
from flask_login import login_required
from ...core.auth import admin_required
from .views import (
    analytics_dashboard, user_analytics, account_analytics,
    list_users, create_user, user_accounts,
    list_presets, create_preset
)

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Analytics routes
bp.add_url_rule('/analytics', 'analytics.dashboard',
                view_func=login_required(admin_required(analytics_dashboard)))
bp.add_url_rule('/analytics/user/<user_id>', 'analytics.user_analytics',
                view_func=login_required(user_analytics))
bp.add_url_rule('/analytics/account/<int:account_id>', 'analytics.account_analytics',
                view_func=login_required(account_analytics))

# User management routes
bp.add_url_rule('/users', 'list_users',
                view_func=login_required(admin_required(list_users)))
bp.add_url_rule('/users/create', 'create_user',
                view_func=login_required(admin_required(create_user)),
                methods=['GET', 'POST'])
bp.add_url_rule('/users/<user_id>/accounts', 'user_accounts',
                view_func=login_required(admin_required(user_accounts)))

# Preset management routes
bp.add_url_rule('/presets', 'list_presets',
                view_func=login_required(admin_required(list_presets)))
bp.add_url_rule('/presets/create', 'create_preset',
                view_func=login_required(admin_required(create_preset)),
                methods=['GET', 'POST'])