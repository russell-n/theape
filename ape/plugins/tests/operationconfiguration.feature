Feature: Operation Configuration
 Scenario: User builds Operation Configuration
  Given a configuration with operations and plugins for the operation configuration
  When a user builds the operation configuration
  Then the operation configuration has the plugins
