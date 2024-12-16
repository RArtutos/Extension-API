from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length
from datetime import datetime, timedelta

class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    is_admin = BooleanField('Is Admin')
    valid_period = SelectField('Valid For', choices=[
        ('7', '7 days'),
        ('30', '30 days'),
        ('90', '90 days'),
        ('365', '1 year'),
        ('-1', 'Never expires')
    ], default='30')

    def get_valid_until(self):
        days = int(self.valid_period.data)
        if days == -1:
            return None
        return datetime.utcnow() + timedelta(days=days)