from flask import render_template
from flask_login import login_required
from ...core.auth import admin_required
from ...services.admin import AdminService

admin_service = AdminService()

def analytics_dashboard():
    """Get general analytics dashboard"""
    analytics_data = admin_service.get_analytics()
    return render_template('admin/analytics.html', analytics=analytics_data)

def user_analytics(user_id):
    """Get analytics for a specific user"""
    analytics_data = admin_service.get_user_analytics(user_id)
    return render_template('analytics/user_dashboard.html', analytics=analytics_data)

def account_analytics(account_id):
    """Get analytics for a specific account"""
    analytics_data = admin_service.get_account_analytics(account_id)
    return render_template('analytics/account_dashboard.html', analytics=analytics_data)