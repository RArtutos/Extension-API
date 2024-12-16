from flask import render_template, redirect, url_for, flash, request, jsonify
from ...services.admin import AdminService
from ...forms.preset import PresetForm

admin_service = AdminService()

def list_presets():
    presets = admin_service.get_presets()
    return render_template('admin/presets/list.html', presets=presets)

def create_preset():
    form = PresetForm()
    if form.validate_on_submit():
        try:
            preset_data = {
                'name': form.name.data,
                'description': form.description.data,
                'account_ids': form.account_ids.data
            }
            admin_service.create_preset(preset_data)
            flash('Preset created successfully', 'success')
            return redirect(url_for('admin.list_presets'))
        except Exception as e:
            flash(str(e), 'error')
    return render_template('admin/presets/form.html', form=form, is_edit=False)

def edit_preset(preset_id):
    preset = admin_service.get_preset(preset_id)
    if not preset:
        flash('Preset not found', 'error')
        return redirect(url_for('admin.list_presets'))

    form = PresetForm(obj=preset)
    if form.validate_on_submit():
        try:
            preset_data = {
                'name': form.name.data,
                'description': form.description.data,
                'account_ids': form.account_ids.data
            }
            admin_service.update_preset(preset_id, preset_data)
            flash('Preset updated successfully', 'success')
            return redirect(url_for('admin.list_presets'))
        except Exception as e:
            flash(str(e), 'error')

    return render_template('admin/presets/form.html', form=form, is_edit=True)

def delete_preset(preset_id):
    try:
        if admin_service.delete_preset(preset_id):
            return jsonify({'success': True, 'message': 'Preset deleted successfully'})
        return jsonify({'success': False, 'message': 'Failed to delete preset'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500