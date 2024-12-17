from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange

class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    is_admin = BooleanField('Is Admin')
    expires_in_days = IntegerField('Expires In (Days)', 
                                 validators=[Optional(), NumberRange(min=1)],
                                 default=30)
    preset_id = SelectField('Preset', 
                          validators=[Optional()],
                          coerce=int,
                          choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from ..services.admin import AdminService
        admin_service = AdminService()
        try:
            presets = admin_service.get_presets()
            self.preset_id.choices = [(0, 'None')] + [(p['id'], p['name']) for p in presets]
        except Exception:
            self.preset_id.choices = [(0, 'None')]