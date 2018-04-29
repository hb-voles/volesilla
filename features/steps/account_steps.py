"""Account impl."""

from behave import given, when, then  # pylint: disable=no-name-in-module
from bs4 import BeautifulSoup
from hamcrest import assert_that, equal_to

from database import init_db, check_db_created, add_user, check_user_added, check_active_token_exist
from server import start_server

from app.extensions import MAIL

# pylint: disable=function-redefined


@given(u'we have vls running with admin user "{user_mail}"')
def step_impl(context, user_mail):
    """Run vls server with admin user"""

    proc_init, db_file = init_db(context.scenario_test_dir)
    check_db_created(proc_init, db_file)

    proc_add_user = add_user(db_file, user_mail)
    check_user_added(proc_add_user, db_file, user_mail)

    context.vls = start_server(context.scenario_test_dir, db_file)


@when(u'we ask for password reset for user "{user_mail}"')
def step_impl(context, user_mail):
    """Ask for password reset"""

    response = context.vls['client'].get('/password/forgotten')
    soup = BeautifulSoup(response.data, 'html.parser')
    csrf = soup.find('input', {'id': 'csrf_token'})

    with MAIL.record_messages() as outbox:

        context.vls['response'] = context.vls['client'].post('/password/forgotten', data=dict(
            csrf_token=csrf['value'],
            email=user_mail,
        ), follow_redirects=True)

        context.vls['outbox'] = outbox


@then(u'there is active "{token_type}" token for user "{user_mail}"')
def step_impl(context, token_type, user_mail):
    """Check there is active reset-password token"""

    context.vls['tokens'] = check_active_token_exist(context.vls['db_file'], token_type, user_mail)

    assert_that(len(context.vls['tokens']), equal_to(1))


@then(u'account "{user_mail}" received reset-password mail with proper token')
def step_impl(context, user_mail):
    """Check reset-password mail"""

    assert_that(len(context.vls['outbox']), equal_to(1))
    assert_that(context.vls['outbox'][0].sender, equal_to('Hell-Bent VoleS <>'))
    assert_that(len(context.vls['outbox'][0].recipients), equal_to(1))
    assert_that(str(context.vls['outbox'][0].recipients[0]), equal_to(user_mail))
    assert_that(context.vls['outbox'][0].subject, equal_to(
        '[voles.cz] Confirmation of Password Reset'))
    assert_that(context.vls['tokens'][0]['token_uid']
                in context.vls['outbox'][0].body, equal_to(True))
