Feature: Simple

  Scenario: Homepage is accessible
    Given we have vls running with basic configuration
    When we access "/"
    Then return status is "200"
