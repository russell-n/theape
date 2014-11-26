
# third party
from behave import given, when, then
from hamcrest import assert_that, calling, raises, is_, instance_of
from configobj import ConfigObj
from validate import Validator

# this package
from ape.plugins.base_plugin import BaseConfiguration


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


class FakeConfiguration(BaseConfiguration):
    def __init__(self, *args, **kwargs):
        super(FakeConfiguration, self).__init__(*args, **kwargs)
        return

    @property
    def product(self):
        return

config = """
[FAKE]
op = value
""".splitlines()

configspec = """
op = string
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
    context.configuration = context.implementation(configuration=context.configuration,
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
