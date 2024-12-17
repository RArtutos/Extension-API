"""Admin presets views"""
from flask import render_template, redirect, url_for, flash, request, jsonify
from ....services.admin import AdminService
from ....forms.preset import PresetForm
from . import bp

admin_service = AdminService()

@bp.route('/')
def list_presets():
    """List all presets"""
    try:
        presets = admin_service.get_presets()
        return render_template('admin/presets/list.html', presets=presets)
    except Exception as e:
        flash(f'Error loading presets: {str(e)}', 'error')
        return render_template('admin/presets/list.html', presets=[])

@bp.route('/create', methods=['GET', 'POST'])
def create_preset():
    """Create new preset"""
    form = PresetForm()
    if form.validate_on_submit():
        try:
            preset_data = {
                'name': form.name.data,
                'description': form.description.data,
                'account_ids': form.account_ids.data
            }
            if admin_service.create_preset(preset_data):
                flash('Preset created successfully', 'success')
                return redirect(url_for('admin.presets.list_presets'))
            flash('Failed to create preset', 'error')
        except Exception as e:
            flash(str(e), 'error')
    return render_template('admin/presets/form.html', form=form, is_edit=False)

@bp.route('/<int:preset_id>/edit', methods=['GET', 'POST'])
def edit_preset(preset_id):
    """Edit existing preset"""
    preset = admin_service.get_preset(preset_id)
    if not preset:
        flash('Preset not found', 'error')
        return redirect(url_for('admin.presets.list_presets'))

    form = PresetForm()
    if request.method == 'GET':
        form.name.data = preset['name']
        form.description.data = preset.get('description')
        form.account_ids.data = preset.get('account_ids', [])

    if form.validate_on_submit():
        try:
            preset_data = {
                'name': form.name.data,
                'description': form.description.data,
                'account_ids': form.account_ids.data
            }
            if admin_service.update_preset(preset_id, preset_data):
                flash('Preset updated successfully', 'success')
                return redirect(url_for('admin.presets.list_presets'))
            flash('Failed to update preset', 'error')
        except Exception as e:
            flash(str(e), 'error')
    return render_template('admin/presets/form.html', form=form, is_edit=True)

@bp.route('/<int:preset_id>', methods=['DELETE'])
def delete_preset(preset_id):
    """Delete preset"""
    try:
        if admin_service.delete_preset(preset_id):
            return jsonify({'success': True, 'message': 'Preset deleted successfully'})
        return jsonify({'success': False, 'message': 'Failed to delete preset'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500