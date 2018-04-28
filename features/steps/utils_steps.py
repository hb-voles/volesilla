"""Simple impl."""

import os
import subprocess
import sqlite3
from behave import given, when, then  # pylint: disable=no-name-in-module

# pylint: disable=function-redefined


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


@when(u'we run volesilla_utils db_init')
def step_impl(context):
    """Create database"""

    context.proc, context.db_file = init_db(context.scenario_test_dir)


@then(u'database file is created')
def step_impl(context):
    """Check if database was created"""

    check_db_created(context.proc, context.db_file)


@given(u'database file is created')
def step_impl(context):
    """Creation of database file"""

    proc, db_file = init_db(context.scenario_test_dir)
    check_db_created(proc, db_file)

    context.db_file = db_file


@when(u'we run volesilla_utils db_add_user "{user_mail}"')
def step_impl(context, user_mail):
    """Add user into database"""

    context.proc = add_user(context.db_file, user_mail)


@then(u'user "{user_mail}" is added')
def step_impl(context, user_mail):
    """Check if user was created"""

    check_user_added(context.proc, context.db_file, user_mail)
