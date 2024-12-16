from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from ...core.auth import admin_required
from ...services.groups import GroupService
from .. import groups

bp = groups.bp
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