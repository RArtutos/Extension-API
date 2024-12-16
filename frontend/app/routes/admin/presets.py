from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from ...core.auth import admin_required
from ...services.admin import AdminService
from ...forms.preset import PresetForm

bp = Blueprint('presets', __name__, url_prefix='/admin/presets')
admin_service = None

def get_admin_service():
    global admin_service
    if admin_service is None:
        admin_service = AdminService()
    return admin_service

@bp.route('/')
@login_required
@admin_required
def list_presets():
    service = get_admin_service()
    presets = service.get_presets()
    return render_template('admin/presets/list.html', presets=presets)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_preset():
    form = PresetForm()
    if form.validate_on_submit():
        try:
            service = get_admin_service()
            preset_data = {
                'name': form.name.data,
                'description': form.description.data,
                'account_ids': form.account_ids.data
            }
            service.create_preset(preset_data)
            flash('Preset created successfully', 'success')
            return redirect(url_for('.list_presets'))
        except Exception as e:
            flash(str(e), 'error')
    return render_template('admin/presets/form.html', form=form, is_edit=False)

@bp.route('/<int:preset_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_preset(preset_id):
    service = get_admin_service()
    preset = service.get_preset(preset_id)
    if not preset:
        flash('Preset not found', 'error')
        return redirect(url_for('.list_presets'))

    form = PresetForm(obj=preset)
    if form.validate_on_submit():
        try:
            preset_data = {
                'name': form.name.data,
                'description': form.description.data,
                'account_ids': form.account_ids.data
            }
            service.update_preset(preset_id, preset_data)
            flash('Preset updated successfully', 'success')
            return redirect(url_for('.list_presets'))
        except Exception as e:
            flash(str(e), 'error')

    return render_template('admin/presets/form.html', form=form, is_edit=True)

@bp.route('/<int:preset_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_preset(preset_id):
    try:
        service = get_admin_service()
        if service.delete_preset(preset_id):
            return jsonify({'success': True, 'message': 'Preset deleted successfully'})
        return jsonify({'success': False, 'message': 'Failed to delete preset'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500