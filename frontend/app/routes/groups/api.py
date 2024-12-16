from flask import jsonify, request
from flask_login import login_required
from ...core.auth import admin_required
from ...services.groups import GroupService
from .. import groups

bp = groups.bp
group_service = GroupService()

@bp.route('/api/list', methods=['GET'])
@login_required
def list_groups():
    try:
        groups = group_service.get_all()
        return jsonify(groups)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/create', methods=['POST'])
@login_required
@admin_required
def create_group():
    try:
        data = request.get_json()
        if not data or not data.get('name'):
            return jsonify({'error': 'Group name is required'}), 400
            
        result = group_service.create(data)
        if result:
            return jsonify(result)
        return jsonify({'error': 'Failed to create group'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/<int:group_id>/accounts/<int:account_id>', methods=['POST'])
@login_required
@admin_required
def assign_account(group_id: int, account_id: int):
    try:
        if group_service.assign_account(group_id, account_id):
            return jsonify({'message': 'Account assigned successfully'})
        return jsonify({'error': 'Failed to assign account'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500