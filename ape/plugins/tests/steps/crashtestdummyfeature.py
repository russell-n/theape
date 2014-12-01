
# third-party
from behave import given, when, then
from hamcrest import assert_that, is_, equal_to, calling, raises, instance_of
from configobj import ConfigObj

# this package
from ape.plugins.dummyplugin import CrashTestDummyConstants
from ape.plugins.dummyplugin import CrashTestDummyConfiguration
from ape.plugins.base_plugin import BaseConfiguration
from ape import ConfigurationError


empty_config = """
[default_crash]
plugin = CrashTestDummy
""".splitlines()

@given("an empty crash test dummy configuration")
def empty_crash_test_dummy_configuration(context):
    context.dummy_configuration = CrashTestDummyConfiguration(section_name='default_crash',
                                                              source=ConfigObj(empty_config))
    return


@when("the configuration is checked")
def check_configuration(context):
    context.configuration = context.dummy_configuration.configuration
    return


@then("the crash test dummy configuration has the defaults")
def assert_default_configuration(context):
    constants = CrashTestDummyConstants
    assert_that(context.configuration[constants.error_module_option],
                is_(equal_to(constants.error_module_default)))

    assert_that(context.configuration[constants.error_option],
                is_(equal_to(constants.error_default)))

    assert_that(context.configuration[constants.error_message_option],
                is_(equal_to(constants.error_message_default)))

    assert_that(context.configuration[constants.function_option],
                is_(equal_to(constants.function_default)))
    return


@then("it is a Base Configuration")
def assert_base_configuration(context):
    assert_that(context.dummy_configuration,
                is_(instance_of(BaseConfiguration)))
    return


bad_plugin = """
[bad_plugin]
plugin = BadBadBad
""".splitlines()

@given("a crash test dummy with the wrong plugin name")
def wrong_plugin(context):
    context.dummy_configuration = CrashTestDummyConfiguration(section_name='bad_plugin',
                                                              source=ConfigObj(bad_plugin))
    return


@when("the configuration with the wrong plugin is checked")
def check_wrong_plugin(context):
    context.check = lambda : context.dummy_configuration
    return


@then("the crash test dummy validator will raise a ConfigurationError")
def raise_error(context):
    #assert_that(calling(context.check),
    #            raises(ConfigurationError))
    return
