"""Data model for user"""

import uuid
from datetime import datetime
from flask import session

from app.extensions import flask_bcrypt, db
from app.account.model import User
from app.account.model import Invite


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


def create_invite_token(valid_until, created_by, for_user):
    '''Save invite_token into DB'''

    invite = Invite(
        token=uuid.uuid4().hex,
        valid_until=valid_until,
        created_by=created_by,
        for_user=for_user)

    db.session.add(invite)
    db.session.commit()


def validate_invite_token(invite_token):
    '''Return True if invite token is valid else False'''

    invite = Invite.query.filter_by(token=invite_token).first()

    if invite:
        return (invite.valid_until > datetime.now()) and invite.active

    return False


def create_account(username, password, email, invite_token, confirmed_at):
    '''Create new user account'''

    token = Invite.query.filter_by(token=invite_token).first()
    token.active = False

    user = User(
        username=username,
        password=flask_bcrypt.generate_password_hash(password),
        email=email,
        confirmed_at=confirmed_at,
        active=True)

    db.session.add(token)
    db.session.add(user)
    db.session.commit()
