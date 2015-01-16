Operation Configuration
=======================

.. literalinclude:: ../operationconfiguration.feature
   :language: gherkin




Scenario: User builds Operation Configuration
---------------------------------------------


.. code:: python

    config_file = """
    [OPERATIONS]
    op1 = p2, p3
    
    [PLUGINS]
     [[p2]]
     plugin = Fake
    
     option1 = value1
    
     [[p3]]
     plugin = Fakir
    
     option1 = value2
    """.splitlines()
    
    @given("a configuration with operations and plugins for the operation configuration")
    def configuration(context):
        context.operator_configuration = OperatorConfiguration(config_file)
        context.configobj = context.operator_configuration.configuration
        context.section = context.configobj['PLUGINS']   
        return




.. code:: python

    @when("a user builds the operation configuration")
    def build_operation_configuration(context):
        context.operation_name = 'op1'
        context.plugin_sections = context.configobj['OPERATIONS'][context.operation_name]
        context.quartermaster = MagicMock()
        context.operation_configuration = OperationConfiguration(plugins_section=context.section,
                                                                 plugin_subsections=context.plugin_sections,
                                                                 operation_name=context.operation_name,
                                                                 quartermaster=context.quartermaster)
        #print context.configobj
        return




.. code:: python

    @then("the operation configuration has the plugins")
    def check_plugins(context):
        assert_that(context.operation_configuration,
                    is_(instance_of(OperationConfiguration)))
        assert_that(context.operation_configuration.operation_name,
                    is_(context.operation_name))
    
        assert_that(context.operation_configuration.plugin_subsections,
                    contains('p2', 'p3'))
    
        expected = dict(zip('p2 p3'.split(), 'Fake Fakir'.split()))
        #assert_that(context.operation_configuration.plugin_names,
        #            contains('Fake', 'Fakir'))
        assert_that(context.operation_configuration.plugin_sections_names,
                    has_entries(expected))
    
        fake_definition = MagicMock(name='fake')
        fake_plugin = MagicMock(name='fake_plugin')
        fake_definition.return_value = fake_plugin
    
        
        fakir_definition = MagicMock(name='fakir')
        fakir_plugin = MagicMock(name='fakir_plugin')
    
        fakir_definition.return_value = fakir_plugin
        
        p_dict = dict(zip('Fake Fakir'.split(), (fake_definition, fakir_definition)))
        
        get_plugin = lambda name: p_dict[name]
        
        context.quartermaster.get_plugin.side_effect = get_plugin
    
        context.operation_configuration.operation
        fake_definition.assert_called_with(configuration=context.operation_configuration.plugins_section,
                                section_header='p2')
        fakir_definition.assert_called_with(configuration=context.operation_configuration.plugins_section,
                                section_header='p3')
    
        assert_that(context.operation_configuration.operation.components,
                    contains(fake_plugin.product, fakir_plugin.product))
        return


