from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from ..services.accounts import AccountService
from ..forms.account import AccountForm

bp = Blueprint('accounts', __name__)
account_service = AccountService()

@bp.route('/')
@login_required
def list():
    try:
        accounts = account_service.get_all()
        return render_template('accounts/list.html', accounts=accounts)
    except Exception as e:
        flash(f'Error loading accounts: {str(e)}', 'error')
        return render_template('accounts/list.html', accounts=[])

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = AccountForm()
    if form.validate_on_submit():
        try:
            account_data = form.get_data()
            account_service.create(account_data)
            flash('Account created successfully', 'success')
            return redirect(url_for('accounts.list'))
        except Exception as e:
            flash(str(e), 'error')
    
    return render_template('accounts/form.html', form=form)

@bp.route('/<int:account_id>/delete', methods=['POST'])
@login_required
def delete(account_id):
    try:
        if account_service.delete(account_id):
            flash('Account deleted successfully', 'success')
        else:
            flash('Failed to delete account', 'error')
    except Exception as e:
        flash(f'Error deleting account: {str(e)}', 'error')
    
    return redirect(url_for('accounts.list'))