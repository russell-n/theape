The Dummy Plugin
================

.. _dummy-plugin:
The :ref:`DummyClass <dummy-class>` does not do anything. It is meant to be used to test the infrastructure.



.. uml::

   Dummy -|> BasePlugin
   Dummy o- HelpPage

.. currentmodule:: ape.plugins.dummyplugin
.. autosummary::
   :toctree: api

   Dummy
   Dummy.help
   Dummy.sections
   Dummy.product
   Dummy.fetch_config   



Crash-Test-Dummy
----------------

This is a dummy that crashes when called. The config-file should specify which error to raise::

   [CRASHTESTDUMMY]   
   error_module = ape.infrastructure.errors
   error = ApeError
   function = __call__

.. autosummary::
   :toctree: api

   CrashTestDummy
   


Stuck Dummy
-----------

This is a dummy that hangs when called.

.. autosummary::
   :toctree: api

   StuckDummy



The Dummy Products
------------------

DummyClass
~~~~~~~~~~

.. currentmodule:: ape.parts.dummy.dummy
.. autosummary::
   :toctree: api
   
   DummyClass
   DummyClass.__call__

CrashDummy
~~~~~~~~~~

.. autosummary::
   :toctree: api

   CrashDummy
   CrashDummy.__call__

HangingDummy
~~~~~~~~~~~~

.. autosummary::
   :toctree: api

   HangingDummy
   HangingDummy.__call__

