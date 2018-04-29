Feature: Account

  Scenario: Ask for password reset
    Given we have vls running with admin user "admin@test.vls"
    When we ask for password reset for user "admin@test.vls"
    Then return status is "200"
    And we can see "Check your mail" on loaded page
    And there is active "reset-password" token for user "admin@test.vls"
    And account "admin@test.vls" received reset-password mail with proper token

  Scenario: Ask for password reset with unregistered user
    Given we have vls running with admin user "admin@test.vls"
    When we ask for password reset for user "unregistered_user@test.vls"
    Then return status is "200"
    And we can see "Given e-mail isn&#39;t registered!" on loaded page
    And there is no active "reset-password" token for user "admin@test.vls"
    And no mail was sent