from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import login_required
from ..core.auth import admin_required
from ..services.groups import GroupService

bp = Blueprint('groups', __name__, url_prefix='/groups')
group_service = GroupService()

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            description = request.form.get('description')
            
            if not name:
                flash('Group name is required', 'error')
                return redirect(url_for('accounts.list'))
                
            result = group_service.create({
                'name': name,
                'description': description
            })
            
            if result:
                flash('Group created successfully', 'success')
            else:
                flash('Failed to create group', 'error')
                
            return redirect(url_for('accounts.list'))
        except Exception as e:
            flash(f'Error creating group: {str(e)}', 'error')
            return redirect(url_for('accounts.list'))
            
    return render_template('groups/form.html')

@bp.route('/api/list', methods=['GET'])
@login_required
def list_groups():
    try:
        groups = group_service.get_all()
        return jsonify(groups)
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