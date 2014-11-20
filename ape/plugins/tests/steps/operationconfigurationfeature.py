
#third-party
from mock import MagicMock
from behave import when, then, given
from hamcrest import assert_that, is_, instance_of, contains

# this package
from ape.plugins.apeplugin import OperationConfiguration, OperatorConfiguration


config_file = """
[OPERATIONS]
op1 = p2, p3

 [[p2]]
 plugin = Fake

 option1 = value1

 [[p3]]
 plugin = Fakir

 option1 = value2
""".splitlines()

@given("a configuration with operations and plugins for the operation configuration")
def configuration(context):
    context.section = OperatorConfiguration(config_file).configuration['OPERATIONS']
    return


@when("a user builds the operation configuration")
def build_operation_configuration(context):
    context.operation_name = 'op1'
    context.quartermaster = MagicMock()
    context.operation_configuration = OperationConfiguration(section=context.section,
                                                             operation_name=context.operation_name,
                                                             quartermaster=context.quartermaster)
    return


@then("the operation configuration has the plugins")
def check_plugins(context):
    assert_that(context.operation_configuration,
                is_(instance_of(OperationConfiguration)))
    assert_that(context.operation_configuration.operation_name,
                is_(context.operation_name))

    assert_that(context.operation_configuration.plugin_sections,
                contains('p2', 'p3'))

    assert_that(context.operation_configuration.plugin_names,
                contains('Fake', 'Fakir'))
    return
