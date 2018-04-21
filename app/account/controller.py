"""Data model for user"""

from flask import session

from app.extensions import flask_bcrypt
from app.account.model import User


def authenticate(username, password):
    '''
    Return True (and add username to session) if user is authenticated
    else False
    '''

    user = User.query.filter_by(username=username).first()
    if not user:
        return False

    authenticated = flask_bcrypt.check_password_hash(user.password, password)

    if not authenticated:
        return False

    session['username'] = username

    return True
