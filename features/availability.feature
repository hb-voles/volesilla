Feature: Availability

    Scenario: Homepage is available
        Given we have vls running
        When we access "/"
        Then return status is "200"

    Scenario: Login is available
        Given we have vls running
        When we access "/login"
        Then return status is "200"

    Scenario: Logout is available
        Given we have vls running
        When we access "/logout"
        Then return status is "302"

    Scenario: Forgotten is available
        Given we have vls running
        When we access "/password/forgotten"
        Then return status is "200"
