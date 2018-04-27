"""Simple impl."""

from behave import given, when, then  # pylint: disable=no-name-in-module

from app.app import create_app
from app.settings import TestConfig


# pylint: disable=function-redefined


@given(u'we have vls running with basic configuration')
def step_impl(context):  # pylint: disable=unused-argument
    """Create client"""

    app = create_app(config_object=TestConfig)  # pylint: disable=invalid-name
    context.client = app.test_client()


@when(u'we access "{url}"')
def step_impl(context, url):  # pylint: disable=unused-argument
    """Access url"""

    context.response = context.client.get('/')


@then(u'return status is "{status_code}"')
def step_impl(context, status_code):  # pylint: disable=unused-argument
    """Check status code"""

    assert int(status_code) == context.response.status_code
