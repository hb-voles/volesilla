"""Account impl."""

from behave import given, when, then  # pylint: disable=no-name-in-module
from hamcrest import assert_that, equal_to, contains_string

from database import check_active_token_exist, set_old_confirmed_at, get_confirmed_at, get_password
from server import start_server_with_admin, ask_for_reset_password_token, \
    reset_password_with_token, reset_password, sign_in_user, ask_for_new_invitation

from app.extensions import BCRYPT

# pylint: disable=function-redefined


@given(u'we have vls running with admin user "{user_mail}"')
def step_impl(context, user_mail):
    """Run vls server with admin user"""

    context.vls = start_server_with_admin(context.scenario_test_dir, user_mail)


@when(u'we ask for password reset for user "{user_mail}"')
def step_impl(context, user_mail):
    """Ask for password reset"""

    response, outbox = ask_for_reset_password_token(context.vls['client'], user_mail)
    context.vls['response'] = response
    context.vls['outbox'] = outbox


@then(u'we can see "{text}" on loaded page')
def step_impl(context, text):
    """Check loaded page contains text"""

    assert_that(str(context.vls['response'].data), contains_string(text))


@then(u'there is active "{token_type}" token for user "{user_mail}"')
def step_impl(context, token_type, user_mail):
    """Check there is active token_type token for user"""

    context.vls['tokens'] = check_active_token_exist(context.vls['db_file'], token_type, user_mail)
    assert_that(len(context.vls['tokens']), equal_to(1))


@then(u'there is no active "{token_type}" token for user "{user_mail}"')
def step_impl(context, token_type, user_mail):
    """Check there is no active token_type token for user"""

    context.vls['tokens'] = check_active_token_exist(context.vls['db_file'], token_type, user_mail)
    assert_that(len(context.vls['tokens']), equal_to(0))


@then(u'account "{user_mail}" received "{mail_type}" mail with proper token')
def step_impl(context, user_mail, mail_type):
    """Check reset-password mail"""

    assert_that(len(context.vls['outbox']), equal_to(1))
    assert_that(context.vls['outbox'][0].sender, equal_to('Hell-Bent VoleS <>'))
    assert_that(len(context.vls['outbox'][0].recipients), equal_to(1))
    assert_that(str(context.vls['outbox'][0].recipients[0]), equal_to(user_mail))

    if mail_type == 'reset-password':
        assert_that(context.vls['outbox'][0].subject, equal_to(
            '[voles.cz] Confirmation of Password Reset'))
    if mail_type == 'registration':
        assert_that(context.vls['outbox'][0].subject, equal_to(
            '[voles.cz] Invitation'))

    assert_that(context.vls['tokens'][0]['token_uid']
                in context.vls['outbox'][0].body, equal_to(True))


@then(u'no mail was sent')
def step_impl(context):
    """Check no mail was sent"""
    assert_that(len(context.vls['outbox']), equal_to(0))


@given(u'we have "{token_type}" token for user "{user_mail}"')
def step_impl(context, token_type, user_mail):
    """Obtain reset-password token """

    ask_for_reset_password_token(context.vls['client'], user_mail)
    tokens = check_active_token_exist(context.vls['db_file'], token_type, user_mail)
    assert_that(len(tokens), equal_to(1))

    context.vls['token'] = tokens[0]['token_uid']


@when(u'we reset password to "{password}"')
def step_impl(context, password):
    """Reset password"""

    context.vls['response'] = reset_password_with_token(
        context.vls['client'], context.vls['token'], password)


@given(u'confirmed_at is set old for user "{user_mail}"')
def step_impl(context, user_mail):
    """Set old date in confirmed_at"""

    context.vls['confirmed_at'] = set_old_confirmed_at(context.vls['db_file'], user_mail)


@then(u'confirmed_at is updated for user "{user_mail}"')
def step_impl(context, user_mail):
    """Check confirmed_at is updated"""

    recent_confirmed_at = get_confirmed_at(context.vls['db_file'], user_mail)
    assert context.vls['confirmed_at'] < recent_confirmed_at


@then(u'password of user "{user_mail}" is "{password}"')
def step_impl(context, user_mail, password):
    """Check confirmed_at is updated"""

    current_password = get_password(context.vls['db_file'], user_mail)
    assert_that(BCRYPT.check_password_hash(current_password, password), equal_to(1))


@given(u'we reset password to "{password}" for user "{user_mail}"')
def step_impl(context, password, user_mail):
    """Reset password"""

    reset_password(context.vls['client'], context.vls['db_file'], user_mail, password)


@when(u'user "{user_mail}" sign in with password "{password}"')
def step_impl(context, user_mail, password):
    """Sign in user"""

    context.vls['response'] = sign_in_user(context.vls['client'], user_mail, password)


@then(u'"{token_type}" for user "{user_mail}" is valid (cookie)')
def step_impl(context, token_type, user_mail):
    """Check token cookie"""

    tokens = check_active_token_exist(context.vls['db_file'], token_type, user_mail)
    assert_that(len(tokens), equal_to(1))
    token = tokens[0]['token_uid']

    with context.vls['session'].session_transaction() as sess:
        assert token_type in sess
        assert_that(sess[token_type], equal_to(token))


@given(u'user "{user_mail}" is logged in with password "{password}"')
def step_impl(context, user_mail, password):
    """User id logged in"""

    reset_password(context.vls['client'], context.vls['db_file'], user_mail, password)
    sign_in_user(context.vls['client'], user_mail, password)
    context.vls['user_mail'] = user_mail


@when(u'logged user create invitation for email "{unregistered_mail}" with steam id "{steam_id}"')
def step_impl(context, unregistered_mail, steam_id):
    """Create invitation"""

    context.vls['response'], context.vls['outbox'] = ask_for_new_invitation(
        context.vls['client'], unregistered_mail, steam_id)
