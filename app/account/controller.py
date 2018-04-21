"""Data model for user"""

from app.extensions import flask_bcrypt
from app.account.model import User


def authenticate(name, password):
    '''Return True if user is authenticated else False'''

    user = User.query.filter_by(username=name).first()
    if not user:
        return False

    return flask_bcrypt.check_password_hash(user.password, password)
