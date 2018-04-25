"""Token functions"""

from datetime import datetime, timedelta

from app.extensions import DB
from app.account.model import Token


def create_token(token_type, valid_period, user_uid, note=''):
    """
    Create general token.

    :param token_type: Type of token, see Token.TokenType.
    :param valid_period: How long should be token valid.
    :param user_uid: User who is connected to the token.
    :param note: (optional) Note about reason for this token.
    :return: Newly created token.
    """

    token = Token(
        token_type=token_type,
        created_at=datetime.now(),
        valid_until=datetime.now() + valid_period,
        user_uid=user_uid,
        note=note,
    )

    DB.session.add(token)
    DB.session.commit()

    return token


def verify_token(token):
    """
    Verify token.

    :param token: Token which we would like to verify.
    :return: True if token is valid else False.
    """

    return (token.created_at < datetime.now()) and (
        datetime.now() < token.valid_until) and token.is_active


def verify_token_by_uid(token_uid):
    """
    Verify token by uid.

    :param token_uid: Token which we would like to verify.
    :return: True if token is valid else False
    """

    token = Token.query.filter_by(uid=token_uid).first()

    return verify_token(token) if token else False


def cancel_token(token):
    """
    Cancel the token.

    :param token: Token which we would like to cancel
    """

    token.is_active = False

    DB.session.add(token)
    DB.session.commit()


def create_invitation_token(user_uid, note_for_whom):
    """
    Create new invitation token.

    :param user_uid: User who created token.
    :param note_for_whom: For whom is this token.
    :return: Newly created invitation token.
    """

    return create_token(
        token_type=Token.TokenType.INVITATION.value,
        valid_period=timedelta(days=2),
        user_uid=user_uid,
        note=note_for_whom
    )


def create_reset_pasword_token(user_uid):
    """
    Create new reset-password token.

    :param user_uid: User for whom we would like to reset password.
    :return: Newly created reset-password token.
    """

    return create_token(
        token_type=Token.TokenType.RESET_PASSWORD.value,
        valid_period=timedelta(hours=1),
        user_uid=user_uid
    )
