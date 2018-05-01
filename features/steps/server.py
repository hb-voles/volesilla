"""Server test utils"""

import os
from multiprocessing import Process
from bs4 import BeautifulSoup
from hamcrest import assert_that, equal_to

from app.app import create_app
from app.settings import TestConfig
from app.extensions import MAIL

from database import init_db, check_db_created, add_user, check_user_added, check_active_token_exist


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

    response = client.get('/password/forgotten')
    soup = BeautifulSoup(response.data, 'html.parser')
    csrf = soup.find('input', {'id': 'csrf_token'})

    with MAIL.record_messages() as outbox:

        response = client.post('/password/forgotten', data=dict(
            csrf_token=csrf['value'],
            email=user_mail,
        ), follow_redirects=True)

    return response, outbox


def reset_password_with_token(client, token, password):
    """Reset password via token"""

    response = client.get('/password/reset/{}'.format(token))
    soup = BeautifulSoup(response.data, 'html.parser')
    csrf = soup.find('input', {'id': 'csrf_token'})

    return client.post('/password/reset/{}'.format(token), data=dict(
        csrf_token=csrf['value'],
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

    response = client.get('/login')
    soup = BeautifulSoup(response.data, 'html.parser')
    csrf = soup.find('input', {'id': 'csrf_token'})

    response = client.post('/login', data=dict(
        csrf_token=csrf['value'],
        email=user_mail,
        password=password,
    ), follow_redirects=True)

    return response
