Testing the Command
===================




.. module:: theape.parts.command.tests
.. autosummary:: 
   :toctree: api

   TestTheCommand.test_constructor
   TestTheCommand.test_defaults
   TestTheCommand.test_expressions
   TestTheCommand.test_command_arguments
   TestTheCommand.test_call
   TestTheCommand.test_bad_data_expression
   TestTheCommand.test_timeout
   TestTheCommand.test_error_match
   TestTheCommand.test_not_available





.. autosummary::
   :toctree: api

   random_string_of_letters


.. code:: python

    def random_string_of_letters(length=5):
        return "".join((random.choice(string.letters) for
                        character in xrange(length)))



