"""Admin users views"""
from flask import render_template, redirect, url_for, flash
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
                admin_service.create_user(form.data)
                flash('User created successfully', 'success')
                return redirect(url_for('admin.list_users'))
            except Exception as e:
                flash(str(e), 'error')
        return render_template('admin/users/form.html', form=form)

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