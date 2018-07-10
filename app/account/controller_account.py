"""Account functions"""

from datetime import datetime
import uuid
from flask import current_app

from app.extensions import DB, BCRYPT
from app.database import User, Token, TokenType

from app.account.controller_token import verify_token_by_uid


def create_account(email):
    """
    Create new account.

    :param email: e-mail
    :return: user.uid.hex
    """

    with current_app.app_context():

        user = User(
            password=BCRYPT.generate_password_hash(uuid.uuid4().hex),
            email=email,
            confirmed_at=None,
            gdpr_version=0,
            is_active=True
        )

        try:
            DB.session.add(user)
            DB.session.flush()
            DB.session.commit()
        except Exception as error:  # pylint: disable=broad-except,unused-variable
            current_app.logger.error('Write new account into DB fails! {}'.format(error))

    new_user = User.query.filter_by(email=email).first()

    return new_user


def confirm_account(user):
    """
    Confirm and activate account

    :param user: User
    """

    user.confirmed_at = datetime.now()

    try:
        DB.session.add(user)
        DB.session.commit()
    except Exception as errorr:  # pylint: disable=broad-except,unused-variable
        current_app.logger.error('Account confirmation failed!')


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

        return True

    if verify_token_by_uid(reset_password_token_uid, TokenType.INVITATION):

        user = token.user
        user.password = BCRYPT.generate_password_hash(password)

        DB.session.add(user)
        DB.session.commit()

        return True

    return False
