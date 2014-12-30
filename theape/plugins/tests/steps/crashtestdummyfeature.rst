Crash Test Dummy
================

.. literalinclude:: ../crashtestdummy.feature
   :language: gherkin




Scenario: User doesn't specify any options
------------------------------------------

.. '


.. code:: python

    empty_config = """
    [default_crash]
    plugin = CrashTestDummy
    """.splitlines()
    
    @given("an empty crash test dummy configuration")
    def empty_crash_test_dummy_configuration(context):
        context.dummy_configuration = CrashTestDummyConfiguration(section_name='default_crash',
                                                                  source=ConfigObj(empty_config))
        return




.. code:: python

    @when("the configuration is checked")
    def check_configuration(context):
        context.configuration = context.dummy_configuration.configuration
        return




.. code:: python

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




.. code:: python

    @then("it is a Base Configuration")
    def assert_base_configuration(context):
        assert_that(context.dummy_configuration,
                    is_(instance_of(BaseConfiguration)))
        return



Scenario: User passes in wrong plugin
-------------------------------------


.. code:: python

    bad_plugin = """
    [bad_plugin]
    plugin = BadBadBad
    """.splitlines()
    
    @given("a crash test dummy with the wrong plugin name")
    def wrong_plugin(context):
        context.dummy_configuration = CrashTestDummyConfiguration(section_name='bad_plugin',
                                                                  source=ConfigObj(bad_plugin))
        return




.. code:: python

    @when("the configuration with the wrong plugin is checked")
    def check_wrong_plugin(context):
        context.check = lambda : context.dummy_configuration
        return




.. code:: python

    @then("the crash test dummy validator will raise a ConfigurationError")
    def raise_error(context):
        #assert_that(calling(context.check),
        #            raises(ConfigurationError))
        return



Scenario: User gets CrashTestDummy
----------------------------------


.. code:: python

    plugin_config = """
    [test_dummy]
    plugin = CrashTestDummy
    
    """
    
    @given("a CrashTestDummy Configuration")
    def crash_test_dummy_configuration(context):
        context.configuration = CrashTestDummyConfiguration(section_name='test_dummy',
                                                            source=ConfigObj(plugin_config.splitlines()))
        return




.. code:: python

    @when("the user gets the CrashTestDummy product")
    def crash_test_dummy_product(context):
        return




.. code:: python

    @then("the CrashTestDummy is correctly configured")
    def check_configuration(context):
        assert_that(context.configuration.product,
                    is_(instance_of(CrashDummy)))
        return


