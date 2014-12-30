
# third party
from behave import given, when, then
from hamcrest import assert_that, is_, equal_to
from configobj import ConfigObj

# this package
from ape.plugins.base_plugin import BaseConfiguration


configspec = """
brains = integer
bananas = float(default=1)

[snacks]
pickles = string(default="gherkin")
"""

class FakeConfiguration(BaseConfiguration):
    @property
    def product(self):
        return

    @property
    def configspec_source(self):
        if self._configspec_source is None:
            self._configspec_source = configspec
        return self._configspec_source


source = """
[monkey]
brains = 1
bananas = 9

[snacks]
pickles = dill
""".splitlines()

@given("BaseConfiguration implementation is built")
def step_implementation(context):
    context.configuration = FakeConfiguration(configspec_source=configspec,
                                              section_name='monkey',
                                              source=ConfigObj(source))
    return


@when("the sample configuration is retrieved")
def step_implementation(context):
    return


expected_sample = """[[monkey]]
brains = integer
bananas = float(default=1)

[[[snacks]]]
pickles = string(default="gherkin")
"""
@then("the sample configuration looks as expected.")
def check_sample(context):
    assert_that(context.configuration.sample,
                is_(equal_to(expected_sample)))
    return
