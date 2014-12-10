BaseConfiguration check_rep
===========================

.. literalinclude:: ../baseconfigurationcheckrep.feature
   :language: gherkin

::

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
    



Scenario: User calls check_rep on valid configuration
-----------------------------------------------------

::

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
    

::

    @when("check_rep is called")
    def step_implementation(context):
        context.outcome = context.configuration.check_rep()
        return
    

::

    @then("nothing happens")
    def step_implementation(context):
        assert_that(context.outcome,
                    is_(None))
        return
    



Scenario: User calls check_rep on bad configuration
---------------------------------------------------

::

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
    

::

    @when("check_rep is checked")
    def check_rep_check(context):
        context.callable = context.configuration.check_rep
        return
    

::

    @then("a ConfigurationError is raised")
    def step_implementation(context):
        assert_that(calling(context.callable),
                    raises(ConfigurationError))
        return
    



Scenario: User calls check_rep on configuration with extra values
-----------------------------------------------------------------

::

    extra_option_configuration = """
    [cement]
    plugin = Concrete
    op1 = 53
    op2 = 64
    ummagumma = apple_banana
    """.splitlines()
    
    @given("BaseConfiguration implementation with unknown values")
    def step_implementation(context):
        context.configuration = ConcreteConfiguration(source=ConfigObj(extra_option_configuration),
                                                      section_name='cement')
        return
    


  When check_rep is checked
  Then a ConfigurationError is raised

Scenario: User calls check_rep on configuration with allowed extra values
-------------------------------------------------------------------------

::

    @given("BaseConfiguration implementation with allowed unknown values")
    def allowed_unknowns(context):
        context.configuration = ConcreteConfiguration(source=ConfigObj(extra_option_configuration),
                                                      section_name='cement',
                                                      allow_extras=True)
        return
    



When check_rep is checked

::

    @then("a ConfigurationError not raised")
    def no_error(context):
        context.callable()
        return
    

::

    @then("the extra values are in the configuration")
    def assert_extras(context):
        assert_that(context.configuration.configuration['ummagumma'],
                    is_(equal_to('apple_banana')))
    

