Feature: OperatorConfigSpec
 Scenario: User validates empty settings
  Given an empty configuration file
  When the file is validated by the operator configspec
  Then it has the default settings

 Scenario: User validates filled settings
  Given a configuration file with settings
  When the file is validated by the operator configspec
  Then it has the user settings

 Scenario: User validates operations
  Given a configuration with operations
  When the file is validated by the operator configspec
  Then it has the operations dictionary

 Scenario: User validates plugins
  Given a configuration with plugins
  When the file is validated by the operator configspec
  Then it has the plugins dictionary
