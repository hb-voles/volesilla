"""Database test utils"""

import os
from datetime import datetime, timedelta
import subprocess
import sqlite3

from app.utils import iso2datetime
from app.account.model import TokenType


def init_db(test_dir):
    """Create database"""

    my_env = os.environ.copy()
    my_env["VLS_TESTING"] = "1"

    db_file = os.path.join(test_dir, 'volesilla_test.db')
    proc = subprocess.Popen(['python', 'volesilla_utils.py', 'db_init', db_file], env=my_env)

    return proc, db_file


def check_db_created(proc, db_file):
    """Check databse was created"""

    proc.wait(timeout=3)
    assert proc.returncode == 0
    assert os.path.isfile(db_file)


def add_user(db_file, user_mail):
    """Add user into database"""

    my_env = os.environ.copy()
    my_env["VLS_TESTING"] = "1"

    proc = subprocess.Popen(
        ['python', 'volesilla_utils.py', 'db_add_user', db_file, user_mail],
        env=my_env)

    return proc


def check_user_added(proc, db_file, user_mail):
    """Check user was added"""

    proc.wait(timeout=5)
    assert proc.returncode == 0
    assert os.path.isfile(db_file)

    connection = sqlite3.connect(db_file)

    with connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM user')

        users = cursor.fetchall()

    added = False
    for user in users:
        if user['email'] == user_mail:
            added = True

    assert added


def check_active_token_exist(db_file, token_type, user_mail):
    """Check there is active reset-password token"""

    def get_token_type(token_type):
        """Transform token_type to enum value"""
        if token_type == 'invitation_token':
            token_value = TokenType.INVITATION.value
        if token_type == 'reset-password':
            token_value = TokenType.RESET_PASSWORD.value
        if token_type == 'access_token':
            token_value = TokenType.ACCESS.value
        if token_type == 'renew_access_token':
            token_value = TokenType.RENEW_ACCESS.value
        return token_value

    connection = sqlite3.connect(db_file)

    with connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        query = """
            SELECT token.uid AS token_uid
            FROM token
            JOIN user ON token.user_uid = user.uid
            WHERE user.email = ?
            AND token.is_active = 1
            AND token_type = ?
        """
        cursor.execute(query, (user_mail, get_token_type(token_type)))
        tokens = cursor.fetchall()

    result = []
    for token in tokens:
        result.append(token['token_uid'])

    return tokens


def set_old_confirmed_at(db_file, user_mail):
    """Set old confirmed_at"""

    confirmed_at = datetime.now() - timedelta(days=10)

    connection = sqlite3.connect(db_file)

    with connection:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        query = """
            UPDATE user
            SET confirmed_at = ?
            WHERE user.email = ?
        """

        cursor.execute(query, (confirmed_at, user_mail))

    return confirmed_at


def get_confirmed_at(db_file, user_mail):
    """Set old confirmed_at"""

    connection = sqlite3.connect(db_file)

    with connection:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        query = """
            SELECT confirmed_at
            FROM user
            WHERE user.email = ?
        """

        cursor.execute(query, (user_mail,))
        result = cursor.fetchone()

    return iso2datetime(result['confirmed_at'])


def get_password(db_file, user_mail):
    """Get user password"""

    connection = sqlite3.connect(db_file)

    with connection:

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        query = """
            SELECT password
            FROM user
            WHERE user.email = ?
        """

        cursor.execute(query, (user_mail,))
        result = cursor.fetchone()

    return result['password']
