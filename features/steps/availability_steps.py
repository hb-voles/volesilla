"""Availability impl."""

from hamcrest import assert_that, equal_to
from behave import when, then  # pylint: disable=no-name-in-module

# pylint: disable=function-redefined


@when(u'we access "{url}"')
def step_impl(context, url):  # pylint: disable=unused-argument
    """Access url"""

    context.vls['response'] = context.vls['client'].get(url)


@then(u'return status is "{status_code}"')
def step_impl(context, status_code):  # pylint: disable=unused-argument
    """Check status code"""

    assert_that(context.vls['response'].status_code, equal_to(int(status_code)))
