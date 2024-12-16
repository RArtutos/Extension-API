from flask import Blueprint, jsonify, request
from flask_login import login_required
from ...core.auth import admin_required
from ...services.groups import GroupService

bp = Blueprint('admin_groups', __name__)
group_service = GroupService()

@bp.route('/api/groups', methods=['GET'])
@login_required
@admin_required
def get_groups():
    """Get all groups formatted for admin dropdown"""
    try:
        groups = group_service.get_formatted_groups()
        return jsonify(groups)
    except Exception as e:
        return jsonify({'error': str(e)}), 500