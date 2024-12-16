from flask import Blueprint, jsonify, request
from flask_login import login_required
from ...core.auth import admin_required
from ...services.groups import GroupService
from ...services.admin import AdminService

bp = Blueprint('admin_groups', __name__)
group_service = GroupService()
admin_service = AdminService()

@bp.route('/api/groups', methods=['GET'])
@login_required
def get_groups():
    """Get all groups formatted for dropdown"""
    try:
        groups = group_service.get_formatted_groups()
        return jsonify(groups)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/users/<user_id>/groups/<int:group_id>', methods=['POST'])
@login_required
@admin_required
def assign_group_to_user(user_id: str, group_id: int):
    """Assign all accounts from a group to a user"""
    try:
        result = admin_service.assign_group_to_user(user_id, group_id)
        return jsonify({
            'success': True if result else False,
            'message': 'Group assigned successfully' if result else 'Failed to assign group'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500