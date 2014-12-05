
#third-party
from behave import given, when, then
from hamcrest import assert_that, is_, calling, raises
from configobj import ConfigObj

# this package
from ape.plugins.base_plugin import BaseConfiguration, ConfigurationError


configspec_source = """
plugin = option('Concrete')

op1 = integer
op2 = integer
"""

class ConcreteConfiguration(BaseConfiguration):
    """
    Test configuration
    """
    
    @property
    def configspec_source(self):
        if self._configspec_source is None:
            self._configspec_source = configspec_source
        return self._configspec_source

    @property
    def product(self):
        return


valid_configuration = """
[cement]
plugin = Concrete
op1 = 53
op2 = 64
""".splitlines()

@given("BaseConfiguration implementation with valid configuration")
def step_implementation(context):
    context.configuration = ConcreteConfiguration(source=ConfigObj(valid_configuration),
                                                  section_name='cement')
    return


@when("check_rep is called")
def step_implementation(context):
    context.outcome = context.configuration.check_rep()
    return


@then("nothing happens")
def step_implementation(context):
    assert_that(context.outcome,
                is_(None))
    return


invalid_configuration = """
[konkrete]
plugin = Concrete
op1 = apple
op2 = banana
""".splitlines()

@given("BaseConfiguration implementation with configuration errors")
def step_implementation(context):
    context.configuration = ConcreteConfiguration(source=ConfigObj(invalid_configuration),
                                                  section_name='konkrete')
        
    return


@when("check_rep is checked")
def check_rep_check(context):
    context.callable = context.configuration.check_rep
    return


@then("a ConfigurationError is raised")
def step_implementation(context):
    assert_that(calling(context.callable),
                raises(ConfigurationError))
    return
