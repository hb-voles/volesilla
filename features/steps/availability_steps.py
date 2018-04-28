"""Simple impl."""

import os
from multiprocessing import Process
from hamcrest import assert_that, equal_to
from behave import given, when, then  # pylint: disable=no-name-in-module

from app.app import create_app
from app.settings import TestConfig

# pylint: disable=function-redefined


@given(u'we have vls running')
def step_impl(context):  # pylint: disable=unused-argument
    """Create client"""

    app = create_app(config_object=TestConfig)  # pylint: disable=invalid-name

    context.vls['server'] = Process(target=app.run)
    context.vls['server'].start()

    context.vls['client'] = app.test_client()
    context.vls['session'] = context.vls['client'].__enter__()

    pid_file = open(os.path.join(context.scenario_test_dir, 'flask_server.pid'), 'w')
    pid_file.write(str(context.vls['server'].pid))
    pid_file.close()

    # with context.session.session_transaction() as sess:
    #     sess['key here'] = some_value


@when(u'we access "{url}"')
def step_impl(context, url):  # pylint: disable=unused-argument
    """Access url"""

    context.vls['response'] = context.vls['client'].get(url)


@then(u'return status is "{status_code}"')
def step_impl(context, status_code):  # pylint: disable=unused-argument
    """Check status code"""

    assert_that(context.vls['response'].status_code, equal_to(int(status_code)))
