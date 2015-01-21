BaseConfiguration Sample Configuration
======================================

.. literalinclude:: ../baseconfigurationsampleconfiguration.feature
   :language: gherkin





.. code:: python

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



Scenario: User gets a sample configuration
------------------------------------------


.. code:: python

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




.. code:: python

    @when("the sample configuration is retrieved")
    def step_implementation(context):
        return




.. code:: python

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


