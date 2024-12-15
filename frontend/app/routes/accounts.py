from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from ..services.accounts import AccountService
from ..forms.account import AccountForm

bp = Blueprint('accounts', __name__)
account_service = AccountService()

@bp.route('/')
@login_required
def list():
    accounts = account_service.get_all()
    return render_template('accounts/list.html', accounts=accounts)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = AccountForm()
    if form.validate_on_submit():
        try:
            account_service.create(form.data)
            flash('Account created successfully', 'success')
            return redirect(url_for('accounts.list'))
        except Exception as e:
            flash(str(e), 'error')
    
    return render_template('accounts/form.html', form=form)