Feature: Base Configuration
 Scenario: User instantiates the BaseConfiguration
  Given a BaseConfiguration definition
  When the user instantiates the BaseConfiguration
  Then it raises a TypeError

 Scenario: User instantiates BaseConfiguration implementation
  Given a BaseConfiguration implementation
  When the user instantiates the BaseConfiguration implementation
  Then it has the BaseConfiguration default properties
