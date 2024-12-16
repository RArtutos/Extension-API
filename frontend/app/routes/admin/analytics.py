from flask import render_template
from flask_login import login_required
from ...core.auth import admin_required
from ...services.admin import AdminService
from .. import admin

admin_service = AdminService()

@admin.bp.route('/analytics')
@login_required
@admin_required
def analytics():
    analytics_data = admin_service.get_analytics()
    return render_template('admin/analytics.html', analytics=analytics_data)