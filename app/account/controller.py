"""Data model for user"""

from datetime import datetime
from urllib.parse import urljoin

from flask import current_app, session, render_template, url_for
from flask_mail import Message

from app.extensions import BCRYPT, DB, MAIL
from app.account.model import User, Token, TokenType
from app.account.controller_token import verify_token_by_uid, cancel_token, \
    create_registration_token, create_reset_password_token, create_access_token, \
    create_renew_access_token


def authenticate(email, password):
    """
    Return True (and add username to session) if user is authenticated
    else False
    """

    user = User.query.filter_by(email=email).first()
    if not user:
        return False

    if not user.is_active:
        return False

    is_password_correct = BCRYPT.check_password_hash(user.password, password)
    if not is_password_correct:
        return False

    access_token = create_access_token(user.uid)
    renew_access_token = create_renew_access_token(user.uid)

    session['access_token'] = access_token.uid.hex
    session['renew_access_token'] = renew_access_token.uid.hex
    session['user_email'] = user.email

    return True


def search_user_by_email(email):
    """Search user by e-mail"""

    try:
        user = User.query.filter_by(email=email).first()
    except Exception as error:  # pylint: disable=broad-except,unused-variable
        current_app.logger.error('Function search_user_by_email failed!')

    return user if user else None


def change_password(reset_password_token_uid, password):
    """
    Change password for user connected to reset-password token.

    :param reset_password_token_uid: Token.uid(.hex) which defines user for password change.
    :param password: New password.
    :return: True if change was successful else False
    """

    token = Token.query.filter_by(uid=reset_password_token_uid).first()

    if verify_token_by_uid(reset_password_token_uid, TokenType.RESET_PASSWORD):

        user = token.user
        user.password = BCRYPT.generate_password_hash(password)

        DB.session.add(user)
        DB.session.commit()

        cancel_token(token)

        return True

    return False


def create_account(password, email):
    """
    Create new account.

    :param password: Password.
    :param email: e-mail
    :return: user
    """

    user = User(
        password=BCRYPT.generate_password_hash(password),
        email=email,
        confirmed_at=None,
        gdpr_version=current_app.config['GDPR_VERSION'],
        is_active=False)

    try:
        DB.session.add(user)
        DB.session.commit()
    except Exception as errorr:  # pylint: disable=broad-except,unused-variable
        current_app.logger.error('Write new account into DB fails!')

    return user


def confirm_and_activate_account(user):
    """
    Confirm and activate account

    :param user: User
    """

    user = User(
        confirmed_at=datetime.now(),
        is_active=True)

    try:
        DB.session.add(user)
        DB.session.commit()
    except Exception as errorr:  # pylint: disable=broad-except,unused-variable
        current_app.logger.error('Account confirmation and activation fails!')


def send_registration_mail(user):
    """Send confirmation of registration"""

    registration_token = create_registration_token(user.uid)

    link = urljoin(
        current_app.config['HOME_URL'],
        url_for('account.registration_final', token_uid=registration_token.uid.hex)
    )

    msg = Message()
    msg.sender = 'Hell-Bent VoleS <{}>'.format(current_app.config['MAIL_USERNAME'])
    msg.add_recipient(user.email)
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

    token = create_reset_password_token(user.uid)

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
