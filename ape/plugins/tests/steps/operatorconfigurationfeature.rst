Operator Configuration
======================

.. literalinclude:: ../operatorconfiguration.feature
   :language: gherkin



Scenario: User builds the default configuration
-----------------------------------------------

::

    @given("an empty configuration")
    def empty_configuration(context):
        context.configuration = OperatorConfiguration(source=[''])
        return
    

::

    @when("the user checks the operator configuration")
    def check_configuration(context):
        context.timer_definition = MagicMock(spec=CountdownTimer)
        context.singletons = MagicMock()
        context.quartermaster_definition = MagicMock(spec=QuarterMaster)
    
        with nested(
                patch('ape.parts.countdown.countdown.CountdownTimer', context.timer_definition),
                patch('ape.infrastructure.singletons', context.singletons),
                patch('ape.plugins.quartermaster.QuarterMaster', context.quartermaster_definition)):
            context.timer = context.configuration.countdown_timer
            context.configuration.initialize_file_storage()
            context.operation_timer = context.configuration.operation_timer
            context.quartermaster = context.configuration.quartermaster
            context.operation_configurations = context.configuration.operation_configurations
        return
    

::

    @then("the operator configuration is the default")
    def default_configuration(context):
        constants = OperatorConfigurationConstants
        context.timer_definition.assert_called_with(repetitions=constants.default_repetitions,
                                                end_time=constants.default_end_time,
                                                total_time=constants.default_total_time,
                                                log_level=INFO)
    
        assert_that(context.singletons.get_filestorage.called_with(name=constants.file_storage_name))
    
        context.quartermaster_definition.assert_called_with(external_modules=constants.default_modules)
    
        assert_that(len(context.operation_configurations),
                    is_(0))
        return
    



Scenario: User builds configuration with operations
---------------------------------------------------

::

    configuration = """
    [OPERATIONS]
    op1 = p1
    op2 = p2,p3
    """.splitlines()
    
    @given("a configuration with operations and plugins")
    def configuration_operations(context):
        context.configuration = OperatorConfiguration(configuration)
        return
    


  When the user checks the operator configuration

::

    @then("the operator configuration has the operation configurations")
    def assert_operation_configurations(context):
        constants = OperatorConfigurationConstants
        context.timer_definition.assert_called_with(repetitions=constants.default_repetitions,
                                                end_time=constants.default_end_time,
                                                total_time=constants.default_total_time,
                                                log_level=INFO)
        names = [config.operation_name for config in context.operation_configurations]
        assert_that(names,
                    contains('op1', 'op2'))
    
        return
    

