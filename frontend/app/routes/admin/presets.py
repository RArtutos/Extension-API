from flask import render_template, redirect, url_for, flash
from ...services.admin import AdminService
from ...forms.preset import PresetForm

admin_service = AdminService()

class PresetViews:
    def list_presets(self):
        """List all presets"""
        try:
            presets = admin_service.get_presets()
            return render_template('admin/presets/list.html', presets=presets)
        except Exception as e:
            flash(f'Error loading presets: {str(e)}', 'error')
            return render_template('admin/presets/list.html', presets=[])

    def create_preset(self):
        """Create new preset"""
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
                return redirect(url_for('admin.admin_list_presets'))
            except Exception as e:
                flash(str(e), 'error')
        return render_template('admin/presets/form.html', form=form, is_edit=False)

preset_views = PresetViews()