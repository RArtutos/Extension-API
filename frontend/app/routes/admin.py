from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from ..core.auth import admin_required
from ..services.admin import AdminService
from ..services.groups import GroupService
from ..forms.user import UserForm

bp = Blueprint('admin', __name__, url_prefix='/admin')
admin_service = AdminService()
group_service = GroupService()

@bp.route('/users/<user_id>/accounts')
@login_required
@admin_required
def user_accounts(user_id):
    user = admin_service.get_user(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('admin.list_users'))
        
    accounts = admin_service.get_user_accounts(user_id)
    available_accounts = admin_service.get_available_accounts()
    groups = group_service.get_all()  # Get all available groups
    
    return render_template('admin/users/accounts.html', 
                         user=user, 
                         accounts=accounts,
                         available_accounts=available_accounts,
                         groups=groups)

@bp.route('/users/<user_id>/groups/<int:group_id>', methods=['POST'])
@login_required
@admin_required
def assign_group(user_id, group_id):
    try:
        result = admin_service.assign_group_to_user(user_id, group_id)
        if result:
            return jsonify({'success': True, 'message': 'Group assigned successfully'})
        return jsonify({'success': False, 'message': 'Failed to assign group'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500