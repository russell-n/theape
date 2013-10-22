Errors
======

This is the place for errors that are raised by code in this package. In order to make it easier for the :ref:`Operator <the-operator>` to catch (somewhat) predictable errors all the errors raised by `parts`, `components` and `plugins` should be sub-classes of the `ApeError` and be kept in this module.

Contents::

    * :ref:`ApeError <ape-error>`
    * :ref:`ConfigurationError <configuration-error>`

.. _ape-error:    
The ApeError
------------
    
.. uml::

   ApeError -|> Exception

.. currentmodule:: arachneape.commoncode.errors
.. autosummary::
   :toctree: api

   ApeError
   
.. _ape-error:



.. _configuration-error:
The ConfigurationError
----------------------

.. uml::

   ConfigurationError -|> ApeError

.. autosummary::
   :toctree: api

   ConfigurationError
   


.. _dont-catch-error:

.. autosummary::
   :toctree: api

   DontCatchError

If this exception is trapped, it should never be caught by any of the composites, since ApeError level Exceptions and above are what need to be caught.

