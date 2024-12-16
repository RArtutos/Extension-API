from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from datetime import datetime
from ...core.auth import admin_required
from ...services.admin import AdminService
from ...forms.user import UserForm, UserEditForm
from .. import admin

admin_service = AdminService()

@admin.bp.route('/users')
@login_required
@admin_required
def list_users():
    users = admin_service.get_users()
    # Add expiration info to each user
    for user in users:
        if user.get('expires_at'):
            expires_at = datetime.fromisoformat(user['expires_at'].replace('Z', '+00:00'))
            user['is_expired'] = expires_at < datetime.utcnow()
            if not user['is_expired']:
                days = (expires_at - datetime.utcnow()).days
                user['days_until_expiration'] = days
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
    return render_template('admin/users/form.html', form=form, is_edit=False)

@admin.bp.route('/users/<user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = admin_service.get_user(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('admin.list_users'))
        
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        try:
            admin_service.update_user(user_id, form.data)
            flash('User updated successfully', 'success')
            return redirect(url_for('admin.list_users'))
        except Exception as e:
            flash(str(e), 'error')
            
    return render_template('admin/users/form.html', form=form, user=user, is_edit=True)

@admin.bp.route('/users/<user_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    try:
        if admin_service.delete_user(user_id):
            return jsonify({'success': True, 'message': 'User deleted successfully'})
        return jsonify({'success': False, 'message': 'Failed to delete user'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500