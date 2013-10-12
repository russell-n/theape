The Operator
============

An operator runs an operation. Each operator should may to a single configuration.

The OperatorError
-----------------

The `OperatorError` will be raised if an un-recoverable error is detected.

.. uml::

   OperatorError -|> Exception

.. currentmodule:: arachneape.infrastructure.operator
.. autosummary:: 
   :toctree: api

   OperatorError
   
