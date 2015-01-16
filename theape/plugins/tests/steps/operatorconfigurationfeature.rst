Operator Configuration
======================

.. literalinclude:: ../operatorconfiguration.feature
   :language: gherkin




Scenario: User builds the default configuration
-----------------------------------------------


.. code:: python

    @given("an empty configuration")
    def empty_configuration(context):
        context.configuration = OperatorConfiguration(source=[''])
        return




.. code:: python

    @when("the user checks the operator configuration")
    def check_configuration(context):
        context.timer_definition = MagicMock(spec=CountdownTimer)
        context.singletons = MagicMock()
        context.quartermaster_definition = MagicMock(spec=QuarterMaster)
        context.operation_configuration = MagicMock(spec=OperationConfiguration)
        context.operation = MagicMock()
        context.operation_configuration.return_value = context.operation
    
        with nested(
                patch('ape.parts.countdown.countdown.CountdownTimer', context.timer_definition),
                patch('ape.infrastructure.singletons', context.singletons),
                patch('ape.plugins.quartermaster.QuarterMaster', context.quartermaster_definition),
                patch('ape.plugins.apeplugin.OperationConfiguration', context.operation_configuration)):
            context.timer = context.configuration.countdown_timer
            context.configuration.initialize_file_storage()
            context.operation_timer = context.configuration.operation_timer
            context.quartermaster = context.configuration.quartermaster
            for config in context.configuration.operation_configurations:
                pass
        return




.. code:: python

    @then("the operator configuration is the default")
    def default_configuration(context):
        constants = OperatorConfigurationConstants
        context.timer_definition.assert_called_with(repetitions=constants.default_repetitions,
                                                end_time=constants.default_end_time,
                                                total_time=constants.default_total_time,
                                                log_level=INFO)
    
        assert_that(context.singletons.get_filestorage.called_with(name=constants.file_storage_name))
    
        context.quartermaster_definition.assert_called_with(external_modules=constants.default_modules)
    
        assert_that(len([config for config in context.configuration.operation_configurations]),
                    is_(0))
        return



Scenario: User builds configuration with operations
---------------------------------------------------


.. code:: python

    configuration = """
    [OPERATIONS]
    op1 = p1
    op2 = p2,p3
    
    [PLUGINS]
    # this isn't valid, but the OperatorConfiguration doesn't build plugins anyway
    p1 = 1
    p2 = 2
    p3 = 3
    """.splitlines()
    
    @given("a configuration with operations and plugins")
    def configuration_operations(context):
        context.configuration = OperatorConfiguration(configuration)
        return


  When the user checks the operator configuration


.. code:: python

    @then("the operator configuration has the operation configurations")
    def assert_operation_configurations(context):
        constants = OperatorConfigurationConstants
        context.timer_definition.assert_called_with(repetitions=constants.default_repetitions,
                                                end_time=constants.default_end_time,
                                                total_time=constants.default_total_time,
                                                log_level=INFO)
    
        p_dict = dict(zip('p1 p2 p3'.split(), '1 2 3'.split()))
    
        expected = [call(plugins_section=p_dict,
                         plugin_subsections=['p1'],
                         operation_name='op1',
                         quartermaster=context.configuration.quartermaster,
                         countdown_timer=context.configuration.operation_timer),
                         
                    call(plugins_section=p_dict,
                         plugin_subsections=['p2', 'p3' ],
                         operation_name='op2',
                         quartermaster=context.configuration.quartermaster,
                         countdown_timer=context.configuration.operation_timer)]
        assert_that(context.operation_configuration.mock_calls,
                    is_(equal_to(expected)))
    
        mock_operation_config = MagicMock(name='operation config')
        mock_operation_config_2 = MagicMock(name='operation config')
        mock_operation = MagicMock(name='operation')
        mock_operation_2 = MagicMock()
    
        mock_operation_config.operation = mock_operation
        mock_operation_config_2.operation = mock_operation_2
    
        context.configuration._operation_configurations = [mock_operation_config, mock_operation_config_2]
    
        print(context.configuration.operator.components)
        assert_that(context.configuration.operator.components,
                        contains(mock_operation, mock_operation_2))
        return


