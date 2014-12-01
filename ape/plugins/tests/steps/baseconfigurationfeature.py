
# third party
from behave import given, when, then
from hamcrest import assert_that, calling, raises, is_, instance_of, equal_to
from configobj import ConfigObj
from validate import Validator
from mock import MagicMock

# this package
from ape.plugins.base_plugin import BaseConfiguration, BaseConfigurationConstants
from ape.infrastructure.baseclass import RED_ERROR


@given("a BaseConfiguration definition")
def base_configuration_definition(context):
    context.definition = BaseConfiguration
    return


@when("the user instantiates the BaseConfiguration")
def base_configuration_instantiation(context):
    context.callable = lambda : context.definition()
    return


@then("it raises a TypeError")
def assert_raises(context):
    assert_that(calling(context.callable),
                raises(TypeError))
    return


configspec = """
op = string
op2 = integer
""".splitlines()

class FakeConfiguration(BaseConfiguration):
    def __init__(self, *args, **kwargs):
        super(FakeConfiguration, self).__init__(*args, **kwargs)
        return

    @property
    def product(self):
        return

    @property
    def configspec_source(self):
        if self._configspec_source is None:
            self._configspec_source = configspec
        return self._configspec_source

config = """
[FAKE]
op = value
""".splitlines()



@given("a BaseConfiguration implementation")
def base_configuration_implementation(context):
    context.configuration = ConfigObj(config)
    context.implementation = FakeConfiguration
    context.configspec_source = configspec
    context.section_name = 'FAKE'
    return


@when("the user instantiates the BaseConfiguration implementation")
def base_configuration_implementation_instantiation(context):
    context.configuration = context.implementation(source=context.configuration,
                                                   section_name=context.section_name,
                                                   configspec_source=context.configspec_source)
    return


@then("it has the BaseConfiguration default properties")
def assert_default_properties(context):
    assert_that(context.configuration.configuration,
                is_(instance_of(ConfigObj)))

    assert_that(context.configuration.configspec,
                is_(instance_of(ConfigObj)))

    assert_that(context.configuration.validator,
                is_(instance_of(Validator)))
    return


bad_option_config = """
op = value
op2 = not_integer
""".splitlines()

@given("a BaseConfiguration implementation with a bad option")
def bad_option(context):
    error = MagicMock()
    context.logger = MagicMock()
    context.logger.error = error
    bad_option_message = BaseConfigurationConstants.bad_option_message
    context.expected = RED_ERROR.format(error='ConfigurationError',
                                        message=bad_option_message.format(option='op2',
                                                                          section='FAKE',
                                                                          error='the value "not_integer" is of the wrong type.',
                                                                          option_type='integer'))    
    context.configuration = FakeConfiguration(source=ConfigObj(bad_option_config),
                                              section_name='FAKE')
    context.configuration._logger = context.logger
    return


@when("the BaseConfiguration implementation processes the errors")
def process_errors(context):
    outcome = context.configuration.configuration.validate(context.configuration.validator,
                                                           preserve_errors=True)
    context.configuration.process_errors()
    return


@then("the correct error message is logged")
def check_error_message(context):
    context.logger.error.assert_called_with(context.expected)
    return


missing_option_config = """
[FAKE]
op = value
""".splitlines()

@given("a BaseConfiguration implementation with a missing option")
def missing_option(context):
    error = MagicMock()
    context.logger = MagicMock()
    context.logger.error = error
    missing_option_message = BaseConfigurationConstants.missing_option_message
    context.expected = RED_ERROR.format(error='ConfigurationError',
                                        message=missing_option_message.format(option='op2',
                                                                            section='FAKE',
                                                                            option_type='integer'))    
    context.configuration = FakeConfiguration(source=ConfigObj(missing_option_config),
                                              section_name='FAKE')
    context.configuration._logger = context.logger

    return


# the BaseConfiguration is setting the configuration property using the section name
# so the configspect can't have the top-level section name
subsection_configspec = """
[FAKE]
plugin = string

[[sub_section]]
op1 = integer
""".splitlines()

missing_section_config = """
[FAKE]
plugin = fake_plugin
""".splitlines()

@given("a BaseConfiguration implementation missing the section")
def missing_section(context):
    error = MagicMock()
    context.logger = MagicMock()
    context.logger.error = error
    missing_section_message = BaseConfigurationConstants.missing_section_message
    context.expected = RED_ERROR.format(error='ConfigurationError',
                                        message=missing_section_message.format(section='FAKE,sub_section',
                                                                            error='missing section',
                                                                            plugin='fake_plugin'))
    context.configuration = FakeConfiguration(source=ConfigObj(missing_section_config),
                                              configspec_source=subsection_configspec,
                                              section_name='FAKE')
    context.configuration._logger = context.logger
    return


section_name_configspec = """
[{section_name}]
op1 = integer

[[sub_section]]
op2 = integer
"""

section_name_config = """
[FAKE]
op1 = 1

[[sub_section]]
op2 = 1
""".splitlines()

@given("a BaseConfiguration configspec with section_name")
def configspec_section_name(context):
    context.configuration = FakeConfiguration(source=ConfigObj(section_name_config),
                                              configspec_source=section_name_configspec,
                                              section_name='FAKE')
    context.configuration._logger = MagicMock()
    return


@when("the BaseConfiguration implementation is checked")
def check_implementation(context):
    context.configuration.process_errors()
    return


@then("the configuration outcome is True")
def assert_outcome_true(context):
    assert_that(context.configuration.validation_outcome,
                is_(True))
    return


subsection_only_configspec = """
op1 = integer

[sub_section]
op2 = integer
"""
@given("a BaseConfiguration configspec without top-section")
def configspec_subsection(context):
    context.configuration = FakeConfiguration(source=ConfigObj(section_name_config),
                                              configspec_source=section_name_configspec,
                                              section_name='FAKE')
    context.configuration._logger = MagicMock()

    return


extra_options_config = """
[FAKE]
op1 = 1

[[sub_section]]
op2 = 5
op7 = 0
""".splitlines()

@given("a BaseConfiguration config with options not in the configspec")
def extra_options(context):    
    context.logger = MagicMock()
    context.logger.warning = MagicMock()
    context.configuration = FakeConfiguration(source=ConfigObj(extra_options_config),
                                              configspec_source=section_name_configspec,
                                              section_name='FAKE')
    context.configuration._logger = context.logger
    return


@when("the BaseConfiguration implementation checks extra values")
def check_extra_values(context):
    context.outcome = context.configuration.check_extra_values()
    return


@then("the extra values are logged")
def extra_values_logged(context):
    section = 'FAKE,sub_section'
    item_type = 'option'
    name = 'op7'
    message = BaseConfigurationConstants.extra_message.format(section=section,
                                                              item_type=item_type,
                                                              name=name) + "='0'"
    context.logger.warning.assert_called_with(message)
    return


@then('check_extra_value returns True')
def assert_extra_values(context):
    assert_that(context.outcome,
                is_(True))
    return


no_extra_options_config = """
[FAKE]
op1 = 1

[[sub_section]]
op2 = 5
""".splitlines()

@given("a BaseConfiguration config with no options not in the configspec")
def no_extra_options(context):
    context.logger = MagicMock()
    context.logger.warning = MagicMock()
    context.configuration = FakeConfiguration(source=ConfigObj(no_extra_options_config),
                                              configspec_source=section_name_configspec,
                                              section_name='FAKE')
    context.configuration._logger = context.logger

    return


@then("no extra values are logged")
def no_logging(context):
    assert_that(context.logger.warning.mock_calls,
                is_(equal_to([])))
    return


@then('check_extra_value returns False')
def check_extra_false(context):
    assert_that(context.outcome,
                is_(False))
    return


update_sections_configspec = """
[{section_name}]
updates_section = string(default=None)
op1 = integer

[[sub_section]]
op2 = integer
"""

update_sections_config = """
[FAKE]
op1 = 1

[[sub_section]]
op2 = 5

[FAKE2]
updates_section = FAKE

[[sub_section]]
op2 = 2
""".splitlines()

@given("a BaseConfiguration section that updates another section")
def updates_section(context):
    context.logger = MagicMock()
    context.logger.warning = MagicMock()
    context.configuration = FakeConfiguration(source=ConfigObj(update_sections_config),
                                              configspec_source=section_name_configspec,
                                              section_name='FAKE2')
    context.configuration._logger = context.logger
    return


@when("the BaseConfiguration implementation validates the configuration")
def validate_configuration(context):
    return


@then("the BaseConfiguration implementation will have the updates")
def check_updates(context):
    # this needs to be thought out
    assert_that(context.configuration.configuration['FAKE']['op1'],
                is_(equal_to(1)))
    assert_that(context.configuration.configuration['FAKE2']['sub_section']['op2'],
                is_(equal_to(2)))
    return
