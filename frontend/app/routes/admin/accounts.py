from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import login_required
from ...core.auth import admin_required
from ...services.admin import AdminService
from .. import admin

admin_service = AdminService()

@admin.bp.route('/users/<user_id>/accounts')
@login_required
@admin_required
def user_accounts(user_id):
    try:
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
    except Exception as e:
        flash(f'Error loading user accounts: {str(e)}', 'error')
        return redirect(url_for('admin.list_users'))

@admin.bp.route('/users/<user_id>/accounts/<int:account_id>', methods=['POST'])
@login_required
@admin_required
def assign_account(user_id, account_id):
    try:
        result = admin_service.assign_account_to_user(user_id, account_id)
        if result:
            return jsonify({'success': True, 'message': 'Account assigned successfully'})
        return jsonify({'success': False, 'message': 'Failed to assign account'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@admin.bp.route('/users/<user_id>/accounts/<int:account_id>', methods=['DELETE'])
@login_required
@admin_required
def remove_account(user_id, account_id):
    try:
        result = admin_service.remove_account_from_user(user_id, account_id)
        if result:
            return jsonify({'success': True, 'message': 'Account removed successfully'})
        return jsonify({'success': False, 'message': 'Failed to remove account'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500