from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from ...core.auth import admin_required
from ...services.admin import AdminService
from ...forms.user import UserForm
from .. import admin

admin_service = AdminService()

@admin.bp.route('/users')
@login_required
@admin_required
def list_users():
    users = admin_service.get_users()
    return render_template('admin/users/list.html', users=users)

@admin.bp.route('/users/create', methods=['GET', 'POST'])
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

@admin.bp.route('/users/<user_id>/accounts')
@login_required
@admin_required
def user_accounts(user_id):
    user = admin_service.get_user(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('admin.list_users'))
        
    accounts = admin_service.get_user_accounts(user_id)
    available_accounts = admin_service.get_available_accounts()
    return render_template('admin/users/accounts.html', 
                         user=user, 
                         accounts=accounts,
                         available_accounts=available_accounts)