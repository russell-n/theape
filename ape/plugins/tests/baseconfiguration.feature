Feature: Base Configuration
 Scenario: User instantiates the BaseConfiguration
  Given a BaseConfiguration definition
  When the user instantiates the BaseConfiguration
  Then it raises a TypeError

 Scenario: User instantiates BaseConfiguration implementation
  Given a BaseConfiguration implementation
  When the user instantiates the BaseConfiguration implementation
  Then it has the BaseConfiguration default properties

 Scenario: Option fails validation
   Given a BaseConfiguration implementation with a bad option
   When the BaseConfiguration implementation processes the errors
   Then the correct error message is logged

 Scenario: Missing Option
   Given a BaseConfiguration implementation with a missing option
   When the BaseConfiguration implementation processes the errors
   Then the correct error message is logged

 Scenario: Missing Section
   Given a BaseConfiguration implementation missing the section
   When the BaseConfiguration implementation processes the errors
   Then the correct error message is logged
 
 Scenario: ConfigSpec Section Name Format
   Given a BaseConfiguration configspec with section_name
   When the BaseConfiguration implementation is checked
   Then the configuration outcome is True

 Scenario: ConfigSpec string only has sub-section definition
   Given a BaseConfiguration configspec without top-section
   When the BaseConfiguration implementation is checked
   Then the configuration outcome is True

 Scenario: Configuration has extra values
  Given a BaseConfiguration config with options not in the configspec
  When the BaseConfiguration implementation checks extra values
  Then the extra values are logged
  And check_extra_value returns True

 Scenario: Configuration has no extra values
  Given a BaseConfiguration config with no options not in the configspec
  When the BaseConfiguration implementation checks extra values
  Then no extra values are logged
  And check_extra_value returns False
  
 Scenario: Section updates configuration
  Given a BaseConfiguration section that updates another section
  When the BaseConfiguration implementation validates the configuration
  Then the BaseConfiguration implementation will have the updates
