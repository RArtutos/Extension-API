"""Admin analytics views"""
from flask import render_template
from ....services.admin.analytics_service import AnalyticsService

analytics_service = AnalyticsService()

class AnalyticsViews:
    def analytics_dashboard(self):
        """Get general analytics dashboard"""
        analytics_data = analytics_service.get_dashboard()
        return render_template('admin/analytics.html', analytics=analytics_data)

    def user_analytics(self, user_id):
        """Get analytics for a specific user"""
        analytics_data = analytics_service.get_user_analytics(user_id)
        return render_template('analytics/user_dashboard.html', analytics=analytics_data)

    def account_analytics(self, account_id):
        """Get analytics for a specific account"""
        analytics_data = analytics_service.get_account_analytics(account_id)
        return render_template('analytics/account_dashboard.html', analytics=analytics_data)

analytics_views = AnalyticsViews()