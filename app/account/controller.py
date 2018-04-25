"""Data model for user"""

import uuid
from urllib.parse import urljoin
from datetime import datetime, timedelta
from flask import current_app, session, render_template, url_for
from flask_mail import Message

from app.extensions import BCRYPT, DB, MAIL
from app.account.model import User, Token
from app.account.controller_token import verify_token_by_uid, cancel_token, create_reset_pasword_token


def authenticate(email, password):
    """
    Return True (and add username to session) if user is authenticated
    else False
    """

    user = User.query.filter_by(email=email).first()
    if not user:
        return False

    authenticated = BCRYPT.check_password_hash(user.password, password)
    if not authenticated:
        return False

    # TODO Fix it according to issue #20
    session['username'] = email

    return True


def search_user_by_email(email):
    """Search user by e-mail"""

    user = User.query.filter_by(email=email).first()

    return user if user else None


def change_password(reset_password_token_uid, password):
    """
    Change password for user connected to reset-password token.

    :param reset_password_token_uid: Token.uid(.hex) which defines user for password change.
    :param password: New password.
    :return: True if change was successful else False
    """

    token = Token.query.filter_by(uid=reset_password_token_uid).first()

    if verify_token_by_uid(reset_password_token_uid):

        user = token.user
        user.password = BCRYPT.generate_password_hash(password)

        DB.session.add(user)
        DB.session.commit()

        cancel_token(token)

        return True

    return False


def create_invite_token(valid_until, created_by, for_user):
    """Save invite_token into DB"""

    # TODO prepsat pres create_token
    invite = Token(
        token=uuid.uuid4().hex,
        valid_until=valid_until,
        created_by=created_by,
        for_user=for_user)

    DB.session.add(invite)
    DB.session.commit()


def validate_invite_token(invite_token):
    """Return True if invite token is valid else False"""

    invite = Token.query.filter_by(token=invite_token).first()

    if invite:
        return (invite.valid_until > datetime.now()) and invite.active

    return False


def create_account(username, password, email, invite_token, confirmed_at):
    """Create new user account"""

    token = Token.query.filter_by(token=invite_token).first()
    token.active = False

    user = User(
        username=username,
        password=BCRYPT.generate_password_hash(password),
        email=email,
        confirmed_at=confirmed_at,
        active=True)

    try:
        DB.session.add(token)
        DB.session.add(user)
        DB.session.commit()
    except Exception as e:
        current_app.logger.error('Write new account into DB fails!')


def send_confirmation_mail(email):
    """Send confirmation of registration"""

    registration = RegistrationToken(
        token=uuid.uuid4().hex,
        created=datetime.now(),
        valid_until=datetime.now() + timedelta(hours=2),
    )

    try:
        DB.session.add(registration)
        DB.session.commit()
    except Exception as e:
        current_app.logger.error('Write new registration token into DB fails!')

    link = urljoin(
        current_app.config['HOME_URL'],
        url_for('account.registration_confirmation_final', token=registration.token)
    )

    msg = Message()
    msg.sender = 'Hell-Bent VoleS <{}>'.format(current_app.config['MAIL_USERNAME'])
    msg.add_recipient(email)
    msg.subject = '[voles.cz] Confirmation of Registration'
    msg.body = render_template(
        'account/registration_confirmation.plain.mail',
        confirmation_link=link)

    MAIL.send(msg)


def send_reset_password_mail(user):
    """
    Send reset-password token via mail.

    :param user: User whom will receive mail with link to reset password
    """

    token = create_reset_pasword_token(user.uid)

    link = urljoin(
        current_app.config['HOME_URL'],
        url_for('account.reset_password', token_uid=token.uid.hex)
    )

    msg = Message()
    msg.sender = 'Hell-Bent VoleS <{}>'.format(current_app.config['MAIL_USERNAME'])
    msg.add_recipient(user.email)
    msg.subject = '[voles.cz] Confirmation of Password Reset'
    msg.body = render_template(
        'account/reset_password_confirmation.plain.mail',
        reset_password_link=link
    )

    MAIL.send(msg)
