from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange
from datetime import datetime, timedelta

class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    is_admin = BooleanField('Is Admin')
    valid_days = IntegerField('Valid for (days)', 
                            validators=[Optional(), NumberRange(min=1)],
                            default=30,
                            description="Number of days the account will be valid (default: 30 days)")

    def get_expiration_date(self):
        if self.valid_days.data:
            return datetime.utcnow() + timedelta(days=self.valid_days.data)
        return None