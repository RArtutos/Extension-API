```python
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

class AccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    group = StringField('Group')
    domain = StringField('Domain', validators=[DataRequired()])
    cookies = TextAreaField('Cookies')

    def validate_domain(self, field):
        if not field.data:
            return
        
        domain = field.data.strip()
        if not domain.startswith('.') and not domain.startswith('http'):
            field.data = '.' + domain

        if domain.startswith('http'):
            from urllib.parse import urlparse
            domain = urlparse(domain).netloc
            field.data = '.' + domain if not domain.startswith('.') else domain

    def validate_cookies(self, field):
        if not field.data:
            return
            
        try:
            # Guardamos las cookies como un solo valor
            field.processed_cookies = [{
                'domain': self.domain.data.strip(),
                'name': 'header_cookies',  # Nombre fijo para identificar que es un header string
                'value': field.data.strip(),
                'path': '/'
            }]
        except Exception as e:
            raise ValidationError(f'Error processing cookies: {str(e)}')

    def get_data(self):
        """Get form data in the format expected by the API"""
        cookies = getattr(self.cookies, 'processed_cookies', [])
        
        return {
            'name': self.name.data,
            'group': self.group.data or None,
            'cookies': cookies
        }
```