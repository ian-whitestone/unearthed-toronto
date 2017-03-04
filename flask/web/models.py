from flask import url_for, flash
from flask_login import UserMixin, logout_user, current_user

from . import app

class User(UserMixin):
    ''' extend the UserMixin class
            https://flask-login.readthedocs.org/en/latest/_modules/flask_login.html#UserMixin
    '''

    def __init__(self, username):
        self.id = username

    @classmethod
    def get(self, id):
        return self(id)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False