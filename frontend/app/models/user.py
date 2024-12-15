from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email: str, token: str):
        self.email = email
        self.token = token
        
    def get_id(self):
        return self.email