"""Admin users routes"""
from flask import render_template, redirect, url_for, flash, jsonify
from ...services.admin import UserService
from ...forms.user import UserForm
from ...core.auth import admin_required

user_service = UserService()

@admin_required
def list_users():
    """List all users"""
    users = user_service.get_all()
    return render_template('admin/users/list.html', users=users)

@admin_required
def create_user():
    """Create new user"""
    form = UserForm()
    if form.validate_on_submit():
        try:
            user = user_service.create(form.data)
            if user:
                flash('User created successfully', 'success')
                return redirect(url_for('admin.list_users'))
            flash('Failed to create user', 'error')
        except Exception as e:
            flash(str(e), 'error')
    return render_template('admin/users/form.html', form=form)

@admin_required
def user_accounts(user_id: str):
    """Manage user accounts"""
    user = user_service.get_by_id(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('admin.list_users'))
        
    accounts = user_service.get_accounts(user_id)
    available_accounts = user_service.get_available_accounts()
    
    return render_template('admin/users/accounts.html', 
                         user=user, 
                         accounts=accounts,
                         available_accounts=available_accounts)

@admin_required
def assign_account(user_id: str, account_id: int):
    """Assign account to user"""
    try:
        if user_service.assign_account(user_id, account_id):
            return jsonify({'success': True, 'message': 'Account assigned successfully'})
        return jsonify({'success': False, 'message': 'Failed to assign account'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_required
def remove_account(user_id: str, account_id: int):
    """Remove account from user"""
    try:
        if user_service.remove_account(user_id, account_id):
            return jsonify({'success': True, 'message': 'Account removed successfully'})
        return jsonify({'success': False, 'message': 'Failed to remove account'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500