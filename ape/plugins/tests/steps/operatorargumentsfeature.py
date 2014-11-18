
# third-party
from behave import given, when, then
from hamcrest import assert_that, is_
from configobj import ConfigObj

# this package
from ape.plugins.apeplugin import OperatorArgumentsConstants, OperatorArguments


@given("a configuration with an empty APE section")
def empty_ape_section(context):
    context.configuration = ConfigObj(["[APE]"])
    context.arguments = OperatorArguments(configuration=context.configuration)
    return


@when("the OperatorArguments are checked")
def check_operator_arguments(context):
    return


@then("they are the default OperatorArguments")
def assert_default_arguments(context):
  constants = OperatorArgumentsConstants
  assert_that(context.arguments.repetitions,
              is_(constants.default_repetitions))
  return
