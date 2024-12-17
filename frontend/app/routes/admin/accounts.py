"""Admin accounts views"""
from flask import render_template, jsonify
from ...services.admin import AdminService

admin_service = AdminService()

class AccountViews:
    def list_accounts(self):
        """List all accounts (admin only)"""
        accounts = admin_service.get_available_accounts()
        return render_template('admin/accounts/list.html', accounts=accounts)

    def assign_account(self, user_id, account_id):
        """Assign account to user"""
        try:
            if admin_service.assign_account_to_user(user_id, account_id):
                return jsonify({'success': True, 'message': 'Account assigned successfully'})
            return jsonify({'success': False, 'message': 'Failed to assign account'}), 400
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    def remove_account(self, user_id, account_id):
        """Remove account from user"""
        try:
            if admin_service.remove_account_from_user(user_id, account_id):
                return jsonify({'success': True, 'message': 'Account removed successfully'})
            return jsonify({'success': False, 'message': 'Failed to remove account'}), 400
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

account_views = AccountViews()