from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, DateField
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

class UserEditForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)],
                           description="Leave empty to keep current password")
    is_admin = BooleanField('Is Admin')
    expires_at = DateField('Expiration Date', 
                          validators=[Optional()],
                          description="Leave empty for no expiration")

    def get_expiration_date(self):
        if self.expires_at.data:
            # Combine date with end of day time
            return datetime.combine(
                self.expires_at.data, 
                datetime.max.time()
            ).replace(microsecond=0)
        return None