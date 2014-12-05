Feature: BaseConfiguration check_rep method
 Scenario: User calls check_rep on valid configuration
  Given BaseConfiguration implementation with valid configuration
  When check_rep is called
  Then nothing happens

 Scenario: User calls check_rep on bad configuration
  Given BaseConfiguration implementation with configuration errors
  When check_rep is checked
  Then a ConfigurationError is raised
