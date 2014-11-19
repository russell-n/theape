
# python standard library
import random

# third party
from configobj import ConfigObj
from validate import Validator
from behave import given, when, then
from hamcrest import assert_that, is_, equal_to

# this package
from ape.plugins.apeplugin import OperatorConfigspec, OperatorConfigurationConstants
from ape.infrastructure.timemap import RelativeTime, AbsoluteTime


@given("an empty configuration file")
def empty_configuration(context):
    context.configspec = OperatorConfigspec()
    context.configuration = ConfigObj([""],
                                      configspec=context.configspec.configspec)
    return


@when("the file is validated by the operator configspec")
def validate_config(context):
    validator = context.configspec.validator
    context.configuration.validate(validator)
    return


@then("it has the default settings")
def assert_default_settings(context):
    constants = OperatorConfigurationConstants
    settings = context.configuration[constants.settings_section]
    
    assert_that(settings[constants.repetitions_option],
                is_(equal_to(constants.default_repetitions)))
    assert_that(settings[constants.config_glob_option],
                is_(equal_to(constants.default_config_glob)))
    assert_that(settings[constants.total_time_option],
                is_(equal_to(constants.default_total_time)))
    assert_that(settings[constants.end_time_option],
                is_(equal_to(constants.default_end_time)))
    assert_that(settings[constants.subfolder_option],
                is_(equal_to(constants.default_subfolder)))
    assert_that(settings[constants.modules_option],
                is_(equal_to(constants.default_modules)))
    return


configuration = """
[SETTINGS]
repetitions = {rep}
config_glob = {glob}
total_time = {total}
end_time = {abtime}
subfolder = {sub}
external_modules = {mods}
"""

@given("a configuration file with settings")
def configuration_settings(context):    
    context.configspec = OperatorConfigspec()
    context.repetitions = random.randrange(100)
    context.config_glob = 'asonetuglrcg'
    context.subfolder = 'output'
    relative_time = '1 day 3 hours'
    absolute_time = '8:00 pm'
    modules = 'external.module.a,ex.mod.b,emc'
    context.modules = modules.split(',')
    context.total_time = RelativeTime(relative_time)
    ab_time = AbsoluteTime()
    context.end_time = ab_time(absolute_time)
    context.configuration = ConfigObj(configuration.format(rep=context.repetitions,
                                                           glob=context.config_glob,
                                                           total=relative_time,
                                                           abtime=absolute_time,
                                                           sub=context.subfolder,
                                                           mods=modules).splitlines(),
                                      configspec=context.configspec.configspec)

    return


@then("it has the user settings")
def assert_user_settings(context):
    constants = OperatorConfigurationConstants
    settings = context.configuration[constants.settings_section]
    
    assert_that(settings[constants.repetitions_option],
                is_(equal_to(context.repetitions)))
    assert_that(settings[constants.config_glob_option],
                is_(equal_to(context.config_glob)))
    assert_that(settings[constants.total_time_option].total_seconds(),
                is_(equal_to(context.total_time.total_seconds())))
    assert_that(settings[constants.end_time_option],
                is_(equal_to(context.end_time)))

    assert_that(settings[constants.subfolder_option],
                is_(equal_to(context.subfolder)))

    assert_that(settings[constants.modules_option],
                is_(equal_to(context.modules)))

    return
