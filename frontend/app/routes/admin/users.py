"""Admin users views"""
from flask import render_template, redirect, url_for, flash, jsonify, request
from ...services.admin import AdminService
from ...forms.user import UserForm

admin_service = AdminService()

class UserViews:
    def list_users(self):
        """List all users"""
        users = admin_service.get_users()
        return render_template('admin/users/list.html', users=users)

    def create_user(self):
        """Create new user"""
        form = UserForm()
        if form.validate_on_submit():
            try:
                # Convert form data to dict and handle preset_id
                user_data = form.data.copy()
                preset_id = user_data.get('preset_id')
                if preset_id == 0:  # Handle case where '0' is selected as 'None'
                    user_data['preset_id'] = None
                
                user = admin_service.create_user(user_data)
                if user:
                    flash('User created successfully', 'success')
                    return redirect(url_for('admin.list_users'))
                flash('Failed to create user', 'error')
            except Exception as e:
                flash(str(e), 'error')
        return render_template('admin/users/form.html', form=form)

    def assign_account(self, user_id, account_id):
        """Assign account to user"""
        try:
            if admin_service.assign_account_to_user(user_id, account_id):
                return jsonify({'success': True, 'message': 'Account assigned successfully'})
            return jsonify({'success': False, 'message': 'Failed to assign account'}), 400
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    def user_accounts(self, user_id):
        """Manage user accounts"""
        user = admin_service.get_user(user_id)
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('admin.list_users'))
            
        accounts = admin_service.get_user_accounts(user_id)
        available_accounts = admin_service.get_available_accounts()
        return render_template('admin/users/accounts.html', 
                             user=user, 
                             accounts=accounts,
                             available_accounts=available_accounts)

user_views = UserViews()