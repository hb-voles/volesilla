Feature: Availability

    Scenario: Homepage is available
        Given we have vls running with admin user "admin@test.vls"
        When we access "/"
        Then return status is "200"

    Scenario: Login is available
        Given we have vls running with admin user "admin@test.vls"
        When we access "/login"
        Then return status is "200"

    Scenario: Logout is available
        Given we have vls running with admin user "admin@test.vls"
        When we access "/logout"
        Then return status is "302"

    Scenario: Forgotten is available
        Given we have vls running with admin user "admin@test.vls"
        When we access "/password/forgotten"
        Then return status is "200"
