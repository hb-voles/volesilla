"""Authentication functions"""

from flask import current_app, session

from app.extensions import BCRYPT
from app.account.model import User

from app.account.controller_token import create_access_token, create_renew_access_token, \
    search_user_by_token_uid


def authenticate(email, password):
    """
    Return True (and add username to session) if user is authenticated
    else False
    """

    with current_app.app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            return False

        if not user.is_active:
            return False

        is_password_correct = BCRYPT.check_password_hash(user.password, password)
        if not is_password_correct:
            return False

        user_uid = user.uid
        session['user_email'] = user.email

        access_token = create_access_token(user_uid)
        session['access_token'] = access_token.uid.hex

        renew_access_token = create_renew_access_token(user_uid)
        session['renew_access_token'] = renew_access_token.uid.hex

        return True


def get_logged_user():
    """
    Get logged user
    :return: User or None
    """

    with current_app.app_context():
        user = search_user_by_token_uid(session['access_token'])

    return user if user else None
