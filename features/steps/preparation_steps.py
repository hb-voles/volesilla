"""Simple impl."""

import os
from multiprocessing import Process
from behave import given, when, then  # pylint: disable=no-name-in-module

from app.app import create_app
from app.settings import TestConfig

# pylint: disable=function-redefined


@given(u'we have vls running')
def step_impl(context):  # pylint: disable=unused-argument
    """Create client"""

    # with context.session.session_transaction() as sess:
    #     sess['key here'] = some_value

    config = TestConfig
    config.PROJECT_ROOT = context.scenario_test_dir

    app = create_app(config_object=config)  # pylint: disable=invalid-name

    context.server = Process(target=app.run)
    context.server.start()

    context.client = app.test_client()
    context.session = context.client.__enter__()

    server_pid_file = os.path.join(
        context.scenario_test_dir, 'flask_server.pid')

    pid = str(context.server.pid)
    pid_file = open(server_pid_file, 'w')
    pid_file.write(pid)
    pid_file.close()


@given(u'we write user "{user_mail}" into database manually')
def step_impl(context, user_mail):  # pylint: disable=unused-argument
    """Create disable account"""
    pass


@when(u'we access "{url}"')
def step_impl(context, url):  # pylint: disable=unused-argument
    """Access url"""

    context.response = context.client.get(url)


@then(u'return status is "{status_code}"')
def step_impl(context, status_code):  # pylint: disable=unused-argument
    """Check status code"""

    assert int(status_code) == context.response.status_code
