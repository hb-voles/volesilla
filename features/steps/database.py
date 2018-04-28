"""Database test utils"""

import os
import subprocess
import sqlite3


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

    proc.wait(timeout=3)
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
