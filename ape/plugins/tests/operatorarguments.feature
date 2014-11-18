Feature: Operator Arguments
 Scenario: User doesn't configure any operator arguments
  Given a configuration with an empty APE section
  When the OperatorArguments are checked
  Then they are the default OperatorArguments
