Feature: Operator Configuration
 Scenario: User builds the default configuration
  Given an empty configuration
  When the user checks the operator configuration
  Then the operator configuration is the default

 Scenario: User builds configuration with operations
  Given a configuration with operations and plugins
  When the user checks the operator configuration
  Then the operator configuration has the operation configurations
