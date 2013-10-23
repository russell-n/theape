Crash Handler
=============

This is a module to help with catching exceptions.



.. _try-except-decorator:
The try-except Decorator
------------------------

This decorator allows exceptions to be caught and logged, rather than allowing the interpreter to dump the stack-trace (it still logs and displays the stack-trace).

.. autosummary::
   :toctree: api

   try_except
   

This wraps methods, not functions (it uses `self`). `self` must have access to `self.error` (the exception to trap), `self.error_message` a string to put in the title of the error message` and `self.logger` a logging instance to send error messages to. Since it is catching exceptions, any method wrapped with this won't raise an error if the exception in self.error is raised by code it is running.

.. superfluous '

