Feature: BaseConfiguration sample_configuration

 Scenario: User gets a sample configuration
  Given BaseConfiguration implementation is built
  When the sample configuration is retrieved
  Then the sample configuration looks as expected.
