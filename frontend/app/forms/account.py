from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
import json

class AccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    group = StringField('Group')
    cookies = TextAreaField('Cookies')

    def get_data(self):
        data = {
            'name': self.name.data,
            'group': self.group.data or None,
            'cookies': []
        }
        
        if self.cookies.data:
            try:
                cookies_data = json.loads(self.cookies.data)
                if isinstance(cookies_data, list):
                    data['cookies'] = cookies_data
            except json.JSONDecodeError:
                pass
                
        return data