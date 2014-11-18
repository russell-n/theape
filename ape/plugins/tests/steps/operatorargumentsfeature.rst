Operator Arguments
==================

.. literalinclude:: ../operatorarguments.feature
   :language: gherkin



Scenario: User doesn't configure any operator arguments
-------------------------------------------------------
.. '

::

    @given("a configuration with an empty APE section")
    def empty_ape_section(context):
        context.configuration = ConfigObj(["[APE]"])
        context.arguments = OperatorArguments(configuration=context.configuration)
        return
    

::

    @when("the OperatorArguments are checked")
    def check_operator_arguments(context):
        return
    

::

    @then("they are the default OperatorArguments")
    def assert_default_arguments(context):
      constants = OperatorArgumentsConstants
      assert_that(context.arguments.repetitions,
                  is_(constants.default_repetitions))
      return
    

