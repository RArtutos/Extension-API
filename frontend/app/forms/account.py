from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError
from ..utils.cookie_parser import parse_cookie_string

class AccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    group = StringField('Group')
    domain = StringField('Domain', validators=[DataRequired()])
    cookies = TextAreaField('Cookies')

    def validate_domain(self, field):
        if not field.data:
            return
        
        # Basic domain validation
        domain = field.data.strip()
        if not domain.startswith('.') and not domain.startswith('http'):
            field.data = '.' + domain  # Add leading dot for cross-subdomain cookies
        
        # Remove any http/https and get domain
        if domain.startswith('http'):
            from urllib.parse import urlparse
            domain = urlparse(domain).netloc
            field.data = '.' + domain if not domain.startswith('.') else domain

    def validate_cookies(self, field):
        if not field.data:
            return
            
        try:
            cookies = parse_cookie_string(field.data)
            if not cookies:
                raise ValidationError('No valid cookies found in the input')
                
            # Store parsed cookies back in the field
            field.processed_cookies = cookies
            
        except Exception as e:
            raise ValidationError(f'Error processing cookies: {str(e)}')

    def get_data(self):
        """Get form data in the format expected by the API"""
        cookies = getattr(self.cookies, 'processed_cookies', [])
        
        # Add domain to all cookies
        domain = self.domain.data.strip()
        for cookie in cookies:
            cookie['domain'] = domain
            
        return {
            'name': self.name.data,
            'group': self.group.data or None,
            'cookies': cookies
        }