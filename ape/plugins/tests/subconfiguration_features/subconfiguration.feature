Feature: Sub Configuration
 Scenario: User instantiates the SubConfiguration
  Given a SubConfiguration definition
  When the user instantiates the SubConfiguration
  Then it raises a TypeError

 Scenario: User instantiates SubConfiguration implementation
  Given a SubConfiguration implementation
  When the user instantiates the SubConfiguration implementation
  Then it has the SubConfiguration default properties

 Scenario: Option fails validation
   Given a SubConfiguration implementation with a bad option
   When the SubConfiguration implementation processes the errors
   Then the correct error message is logged
   And the process_errors outcome was True

 Scenario: Missing Option
   Given a SubConfiguration implementation with a missing option
   When the SubConfiguration implementation processes the errors
   Then the correct error message is logged

 Scenario: Missing Section
   Given a SubConfiguration implementation missing the section
   When the SubConfiguration implementation processes the errors
   Then the correct error message is logged

 Scenario: Configuration passes
   Given a SubConfiguration implementation with valid configuration
   When the SubConfiguration implementation processes the errors
   Then the process_errors outcome was False
 
 Scenario: ConfigSpec Section Name Format
   Given a SubConfiguration configspec with section_name
   When the SubConfiguration implementation is checked
   Then the configuration outcome is True

 Scenario: ConfigSpec string only has sub-section definition
   Given a SubConfiguration configspec without top-section
   When the SubConfiguration implementation is checked
   Then the configuration outcome is True

 Scenario: Configuration has extra values
  Given a SubConfiguration config with options not in the configspec
  When the SubConfiguration implementation checks extra values
  Then the extra values are logged
  And check_extra_value returns True

 Scenario: Configuration has no extra values
  Given a SubConfiguration config with no options not in the configspec
  When the SubConfiguration implementation checks extra values
  Then no extra values are logged
  And check_extra_value returns False
  
 Scenario: Section updates configuration
  Given a SubConfiguration section that updates another section
  When the SubConfiguration implementation validates the configuration
  Then the SubConfiguration implementation will have the updates

 Scenario: Configuration missing plugin name
  Given a SubConfiguration section missing a required plugin name
  When the SubConfiguration checks process_errors
  Then the process_errors returned True
  And the configuration options that were given are in the configuration
