Feature: Account

  Scenario: Ask for password reset
    Given we have vls running with admin user "admin@test.vls"
    When we ask for password reset for user "admin@test.vls"
    Then return status is "200"
    And there is active "reset-password" token for user "admin@test.vls"
    And account "admin@test.vls" received reset-password mail with proper token
