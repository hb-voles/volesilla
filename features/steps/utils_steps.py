"""Simple impl."""

from behave import given, when, then  # pylint: disable=no-name-in-module
from database import init_db, check_db_created, add_user, check_user_added

# pylint: disable=function-redefined


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
