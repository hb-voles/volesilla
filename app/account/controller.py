"""Data model for user"""

from urllib.parse import urljoin
import requests

from flask import current_app, render_template, url_for
from flask_mail import Message

from app.extensions import DB, MAIL
from app.database import User, Player
from app.account.controller_token import create_reset_password_token


def search_user_by_email(email):
    """Search user by e-mail"""

    with current_app.app_context():
        user = User.query.filter_by(email=email).first()

    return user if user else None


def send_invitation_mail(new_user, player_name, invitation_token_uid):
    """
    Send invitation

    :param new_user: User.
    :param invitation_token: Token.
    """

    link = urljoin(
        current_app.config['HOME_URL'],
        url_for('account.registration_via_token', invitation_token_uid=invitation_token_uid)
    )

    msg = Message()
    msg.sender = 'Hell-Bent VoleS <{}>'.format(current_app.config['MAIL_USERNAME'])
    msg.add_recipient(new_user.email)
    msg.subject = '[voles.cz] Invitation'
    msg.body = render_template(
        'account/registration_confirmation.plain.mail',
        player=player_name,
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


def create_player(user, steam_id, player_name, avatar, avatar_medium, avatar_full):  # pylint: disable=too-many-arguments
    """Create new player"""

    with current_app.app_context():

        player = Player(
            user_uid=user.uid.hex,
            steam_id=steam_id,
            name=player_name,
            avatar=avatar,
            avatar_medium=avatar_medium,
            avatar_full=avatar_full
        )

        try:
            DB.session.add(player)
            DB.session.flush()
            DB.session.commit()
        except Exception as error:  # pylint: disable=broad-except,unused-variable
            current_app.logger.error('Write new player into DB fails! {}'.format(error))

    new_player = Player.query.filter_by(name=player_name).first()

    return new_player


def get_steam_player(steam_id):
    """Get steam player"""

    steam_response = requests.get(
        'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
        params={'key': current_app.config['STEAM_WEB_API_KEY'],
                'steamids': steam_id})

    steam_response.raise_for_status()
    steam_data = steam_response.json()

    return steam_data['response']['players'][0]
