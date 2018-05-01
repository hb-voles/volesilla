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

  Scenario: Reset password
    Given we have vls running with admin user "admin@test.vls"
    and we have "reset-password" token for user "admin@test.vls"
    and confirmed_at is set old for user "admin@test.vls"
    When we reset password to "Password123"
    Then return status is "200"
    And we can see "Successfully Password Changed" on loaded page
    And there is no active "reset-password" token for user "admin@test.vls"
    And confirmed_at is updated for user "admin@test.vls"
    And password of user "admin@test.vls" is "Password123"

  Scenario: Sign in user
    Given we have vls running with admin user "admin@test.vls"
    and we reset password to "Password123" for user "admin@test.vls"
    When user "admin@test.vls" sign in with password "Password123"
    Then return status is "200"
    And cookie contains key "user_email" with value "admin@test.vls"
    And "access_token" for user "admin@test.vls" is valid (cookie)
    And "renew_access_token" for user "admin@test.vls" is valid (cookie)
