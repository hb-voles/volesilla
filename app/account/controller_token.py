"""Token functions"""

from datetime import datetime, timedelta

from flask import current_app, session

from app.extensions import DB
from app.database import Token, TokenType


def create_token(token_type, valid_period, user_uid, note=''):
    """
    Create general token.

    :param token_type: Type of token, see Token.TokenType.
    :param valid_period: How long should be token valid.
    :param user_uid: User who is connected to the token.
    :param note: (optional) Note about reason for this token.
    :return: Newly created token.
    """

    with current_app.app_context():

        token = Token(
            token_type=token_type,
            created_at=datetime.now(),
            valid_until=datetime.now() + valid_period,
            user_uid=user_uid,
            note=note,
        )

        try:
            DB.session.add(token)
            DB.session.flush()
            uid = token.uid
            DB.session.commit()
        except Exception as error:  # pylint: disable=broad-except,unused-variable
            current_app.logger.error('Write new token into DB fails! {}'.format(error))

    new_token = Token.query.filter_by(uid=uid).first()

    return new_token


def cancel_token(token):
    """
    Cancel the token.

    :param token: Token which we would like to cancel
    """

    token.is_active = False

    DB.session.add(token)
    DB.session.commit()


def cancel_token_by_uid(token_uid):
    """
    Cancel token by given token_uid.
    :param token_uid: Given uid.
    """

    token = Token.query.filter_by(uid=token_uid).first()
    cancel_token(token)


def verify_token(token, token_type):
    """
    Verify token.

    :param token: Token which we would like to verify.
    :param token_type: Type of token (TokenType).
    :return: True if token is valid else False.
    """

    return \
        (token.created_at < datetime.now()) and \
        (datetime.now() < token.valid_until) and \
        (token.token_type == token_type.value) and \
        token.is_active


def verify_token_by_uid(token_uid, token_type):
    """
    Verify token by uid.

    :param token_uid: Token which we would like to verify.
    :param token_type: Type of token (TokenType).
    :return: True if token is valid else False
    """

    token = Token.query.filter_by(uid=token_uid).first()

    return verify_token(token, token_type) if token else False


def create_invitation_token(new_user, inviting_user):
    """
    Create new invitation token.

    :param user_uid: User who created token.
    :param note_for_whom: For whom is this token.
    :return: Newly created invitation token.
    """

    return create_token(
        token_type=TokenType.INVITATION.value,
        valid_period=timedelta(days=2),
        user_uid=new_user.uid.hex,
        note=inviting_user.uid.hex,
    )


def create_reset_password_token(user_uid):
    """
    Create new reset-password token.

    :param user_uid: User for whom we would like to reset password.
    :return: Newly created reset-password token.
    """

    return create_token(
        token_type=TokenType.RESET_PASSWORD.value,
        valid_period=timedelta(hours=1),
        user_uid=user_uid
    )


def create_access_token(user_uid):
    """
    Create new access token.

    :param user_uid: User for whom we would like to grant access.
    :return: Newly created access token.
    """

    return create_token(
        token_type=TokenType.ACCESS.value,
        valid_period=timedelta(hours=1),
        user_uid=user_uid
    )


def create_renew_access_token(user_uid):
    """
    Create new renew-access token.

    :param user_uid: User for whom we would like to create renew-access token.
    :return: Newly created renew-access token.
    """

    return create_token(
        token_type=TokenType.RENEW_ACCESS.value,
        valid_period=timedelta(days=2),
        user_uid=user_uid
    )


def search_user_by_token_uid(token_uid):
    """
    Search user connected to token

    :param token_uid: Token uid.
    :return: User if exists and token is active else None
    """

    with current_app.app_context():
        token = Token.query.filter_by(uid=token_uid).first()

        if token:
            return token.user

    return None


def verify_authentication():
    """
    Verifies if user is authenticated (via session)

    :return: True if authenticated else False
    """

    with current_app.app_context():

        if 'access_token' not in session:
            return False

        access_token_uid = session['access_token']
        if verify_token_by_uid(access_token_uid, TokenType.ACCESS):
            return True

        if 'renew_access_token' not in session:
            return False

        renew_access_token_uid = session['renew_access_token']
        if verify_token_by_uid(renew_access_token_uid, TokenType.RENEW_ACCESS):

            user = search_user_by_token_uid(renew_access_token_uid)

            cancel_token_by_uid(renew_access_token_uid)

            access_token = create_access_token(user.uid)
            renew_access_token = create_renew_access_token(user.uid)

            session['access_token'] = access_token.uid.hex
            session['renew_access_token'] = renew_access_token.uid.hex

            return True

        return False
