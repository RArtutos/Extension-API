"""Admin users views"""
from flask import render_template, redirect, url_for, flash, jsonify, request
from ....services.admin import UserService
from ....forms.user import UserForm
from ....core.auth import admin_required
from . import bp

user_service = UserService()

@bp.route('/')
@admin_required
def list_users():
    """List all users"""
    users = user_service.get_all()
    return render_template('admin/users/list.html', users=users)

@bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    """Create new user"""
    form = UserForm()
    if form.validate_on_submit():
        try:
            user_data = {
                'email': form.email.data,
                'password': form.password.data,
                'is_admin': form.is_admin.data,
                'max_devices': form.max_devices.data,
                'expires_in_days': form.expires_in_days.data,
                'preset_id': form.preset_id.data if form.preset_id.data != 0 else None
            }
            
            user = user_service.create(user_data)
            if user:
                flash('User created successfully', 'success')
                return redirect(url_for('admin.users.list_users'))
            flash('Failed to create user', 'error')
        except Exception as e:
            flash(str(e), 'error')
    return render_template('admin/users/form.html', form=form)

@bp.route('/<user_id>/accounts')
@admin_required
def user_accounts(user_id: str):
    """Manage user accounts"""
    user = user_service.get_by_id(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('admin.users.list_users'))
        
    accounts = user_service.get_accounts(user_id)
    available_accounts = user_service.get_available_accounts()
    
    return render_template('admin/users/accounts.html', 
                         user=user, 
                         accounts=accounts,
                         available_accounts=available_accounts)

@bp.route('/<user_id>/accounts/<int:account_id>', methods=['POST'])
@admin_required
def assign_account(user_id: str, account_id: int):
    """Assign account to user"""
    try:
        if user_service.assign_account(user_id, account_id):
            return jsonify({'success': True, 'message': 'Account assigned successfully'})
        return jsonify({'success': False, 'message': 'Failed to assign account'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/<user_id>/accounts/<int:account_id>', methods=['DELETE'])
@admin_required
def remove_account(user_id: str, account_id: int):
    """Remove account from user"""
    try:
        if user_service.remove_account(user_id, account_id):
            return jsonify({'success': True, 'message': 'Account removed successfully'})
        return jsonify({'success': False, 'message': 'Failed to remove account'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id: str):
    """Delete user"""
    try:
        if user_service.delete(user_id):
            return jsonify({'success': True, 'message': 'User deleted successfully'})
        return jsonify({'success': False, 'message': 'Failed to delete user'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500