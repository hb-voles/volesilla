Feature: Volesilla Utils

  Scenario: init_db
    When we run volesilla_utils db_init
    Then database file is created

  Scenario: db_add_user
    Given database file is created
    When we run volesilla_utils db_add_user "admin@test.vls"
    Then user "admin@test.vls" is added
