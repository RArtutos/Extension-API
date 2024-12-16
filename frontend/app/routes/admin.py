from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..services.admin import AdminService
from ..forms.user import UserForm
from ..core.auth import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')
admin_service = AdminService()

@bp.route('/users')
@login_required
@admin_required
def list_users():
    users = admin_service.get_users()
    return render_template('admin/users/list.html', users=users)

@bp.route('/users/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        try:
            admin_service.create_user(form.data)
            flash('User created successfully', 'success')
            return redirect(url_for('admin.list_users'))
        except Exception as e:
            flash(str(e), 'error')
    return render_template('admin/users/form.html', form=form)

@bp.route('/users/<user_id>/accounts')
@login_required
@admin_required
def user_accounts(user_id):
    user = admin_service.get_user(user_id)
    accounts = admin_service.get_user_accounts(user_id)
    available_accounts = admin_service.get_available_accounts()
    return render_template('admin/users/accounts.html', 
                         user=user, 
                         accounts=accounts,
                         available_accounts=available_accounts)

@bp.route('/analytics')
@login_required
@admin_required
def analytics():
    analytics_data = admin_service.get_analytics()
    return render_template('admin/analytics.html', analytics=analytics_data)