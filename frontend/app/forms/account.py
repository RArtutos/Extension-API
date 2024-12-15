from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class AccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    group = StringField('Group')
    cookies = TextAreaField('Cookies')