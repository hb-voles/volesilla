"""Server test utils"""

import os
import json
import requests
from multiprocessing import Process
from bs4 import BeautifulSoup
from hamcrest import assert_that, equal_to
import httpretty

from app.app import create_app
from app.settings import TestConfig
from app.extensions import MAIL

from database import init_db, check_db_created, add_user, check_user_added, check_active_token_exist


def get_csrf(client, url):

    response = client.get(url)
    soup = BeautifulSoup(response.data, 'html.parser')
    csrf = soup.find('input', {'id': 'csrf_token'})

    return csrf['value']


def start_server(test_dir, db_file):  # pylint: disable=unused-argument
    """Run server"""

    vls = {}

    config = TestConfig

    config.RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    config.RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

    config.DB_FILE = db_file
    config.SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(config.DB_FILE)

    vls['db_file'] = db_file

    app = create_app(config_object=config)  # pylint: disable=invalid-name

    vls['server'] = Process(target=app.run)
    vls['server'].start()

    vls['client'] = app.test_client()
    vls['session'] = vls['client'].__enter__()

    pid_file = open(os.path.join(test_dir, 'flask_server.pid'), 'w')
    pid_file.write(str(vls['server'].pid))
    pid_file.close()

    return vls


def start_server_with_admin(test_dir, user_mail):
    """Run vls server with admin user"""

    proc_init, db_file = init_db(test_dir)
    check_db_created(proc_init, db_file)

    proc_add_user = add_user(db_file, user_mail)
    check_user_added(proc_add_user, db_file, user_mail)

    return start_server(test_dir, db_file)


def ask_for_reset_password_token(client, user_mail):
    """Ask for password reset"""

    csrf = get_csrf(client, '/password/forgotten')

    with MAIL.record_messages() as outbox:

        response = client.post('/password/forgotten', data=dict(
            csrf_token=csrf,
            email=user_mail,
        ), follow_redirects=True)

    return response, outbox


def reset_password_with_token(client, token, password):
    """Reset password via token"""

    csrf = get_csrf(client, '/password/reset/{}'.format(token))

    return client.post('/password/reset/{}'.format(token), data=dict(
        csrf_token=csrf,
        password1=password,
        password2=password
    ), follow_redirects=True)


def reset_password(client, db_file, user_mail, password):
    "Reset password"

    ask_for_reset_password_token(client, user_mail)
    tokens = check_active_token_exist(db_file, 'reset-password', user_mail)
    assert_that(len(tokens), equal_to(1))
    token = tokens[0]['token_uid']
    response = reset_password_with_token(client, token, password)
    assert_that(response.status_code, equal_to(200))


def sign_in_user(client, user_mail, password):
    """Ask for password reset"""

    csrf = get_csrf(client, '/login')

    response = client.post('/login', data=dict(
        csrf_token=csrf,
        email=user_mail,
        password=password,
    ), follow_redirects=True)

    return response


def ask_for_new_invitation(client, user_mail, unregistered_mail, steam_id):
    """Ask for password reset"""

    csrf = get_csrf(client, '/invitation/new')

    httpretty.enable()  # enable HTTPretty so that it will monkey patch the socket module

    answer = {'response': {'players': [
        {'steamid': '76561198075520737', 'communityvisibilitystate': 3,
         'profilestate': 1, 'personaname': 'Mol', 'lastlogoff': 1525382474,
         'profileurl': 'https://steamcommunity.com/profiles/76561198075520737/',
         'avatar': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/99/99f5a6a6a9253ab938037afc922d70272c01d24f.jpg',
         'avatarmedium': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/99/99f5a6a6a9253ab938037afc922d70272c01d24f_medium.jpg',
         'avatarfull': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/99/99f5a6a6a9253ab938037afc922d70272c01d24f_full.jpg',
         'personastate': 0, 'realname': 'Petr Čech',
         'primaryclanid': '103582791437981172', 'timecreated': 1352577764,
         'personastateflags': 0, 'loccountrycode': 'CZ'}]}
    }

    httpretty.register_uri(httpretty.GET,
                           "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/",
                           body=json.dumps(answer)
                           )

    response = client.post('/invitation/new', data=dict(
        csrf_token=csrf,
        email=unregistered_mail,
        steam_id=steam_id
    ), follow_redirects=True)

    assert response.status_code == 200

    httpretty.disable()  # disable afterwards, so that you will have no problems in code that uses that socket module
    httpretty.reset()    # reset HTTPretty state (clean up registered urls and request history)

    with MAIL.record_messages() as outbox:

        csrf = get_csrf(client, '/invitation/check')

        response = client.post(
            '/invitation/check',
            data=dict(
                csrf_token=csrf,
                new_user_email=unregistered_mail,
                steam_id=steam_id,
                created_by=user_mail,
                player_name='Mol',
                steam_profile='https://steamcommunity.com/profiles/76561198075520737/',
                avatar='https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/99/99f5a6a6a9253ab938037afc922d70272c01d24f.jpg',
                avatar_medium='https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/99/99f5a6a6a9253ab938037afc922d70272c01d24f_medium.jpg',
                avatar_full='https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/99/99f5a6a6a9253ab938037afc922d70272c01d24f_full.jpg',
            ),
            follow_redirects=True)

        assert_that(response.status_code, equal_to(200))

    return response, outbox
