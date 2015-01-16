The Client Base
===============

Since the SimpleClient and TelnetClient have started to share so much code I'm going to make an abstract base class to try and create a central place for the non-technology-specific code they need.

.. '







.. _clients-base-client:

The BaseClient
--------------

.. module:: theape.clients.clientbase
.. autosummary::
   :toctree: api

   BaseClient




.. _socket-error-decorator:

Socket Decorator
----------------

Since the connections raise socket errors which aren't always easy to interpret, hopefully this will help make it easier to add sensible messages.

.. '

.. autosummary::
   :toctree: api

   handlesocketerrors




.. autosummary::
   :toctree: api

   suppresssocketerrors




.. _simpleclient-connectionerror:

The ConnectionError
-------------------

This is just a sub-class of the `ConnectionError` so anything that traps that will catch it.

.. uml::

   ConnectionError <|-- ConnectionError

.. module:: theape.clients.simpleclient
.. autosummary::
   :toctree: api

   ConnectionError



