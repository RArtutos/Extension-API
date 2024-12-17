"""Admin analytics views"""
from flask import render_template
from ....services.admin import AnalyticsService
from . import bp

analytics_service = AnalyticsService()

@bp.route('/')
def analytics_dashboard():
    """Get general analytics dashboard"""
    analytics_data = analytics_service.get_dashboard()
    return render_template('admin/analytics.html', analytics=analytics_data)

@bp.route('/user/<user_id>')
def user_analytics(user_id):
    """Get analytics for a specific user"""
    analytics_data = analytics_service.get_user_analytics(user_id)
    return render_template('analytics/user_dashboard.html', analytics=analytics_data)

@bp.route('/account/<int:account_id>')
def account_analytics(account_id):
    """Get analytics for a specific account"""
    analytics_data = analytics_service.get_account_analytics(account_id)
    return render_template('analytics/account_dashboard.html', analytics=analytics_data)