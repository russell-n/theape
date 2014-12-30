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



Dummy Configuration
~~~~~~~~~~~~~~~~~~~

This is how the configuration sub-section should appear.

.. language:: ini
.. code-block::

    [[DUMMY]]
    # the section name is arbitrary but must match the name in the [APE] section
    # so the 'plugin' option is what actually specifies the plugin 
    plugin = Dummy
    # the dummy will take anything you set here and log it
    any_arbitrary_option = any_arbitrary_value
    another_option = another_value

Crash-Test-Dummy
----------------

This is a dummy that crashes when called. The config-file should specify which error to raise::

   [[CRASHTESTDUMMY]]
   plugin = CrashTestDummy
   error_message = I have Crashed
   error_module = ape.infrastructure.errors
   error = ApeError
   function = __call__

CrashTestDummyConstants
~~~~~~~~~~~~~~~~~~~~~~~

This is a holder of constants for the CrashTestDummy.

::

    class CrashTestDummyConstants(object):
        __slots__ = ()
        error_module_option = 'error_module'
        error_option = 'error'
        error_message_option = 'error_message'
        function_option = 'function'
        
        error_module_default = 'exceptions'
        error_default = 'Exception'
        error_message_default = 'My work is done, why wait?'
        function_default = '__call__'
    
    



CrashtestConfigspec
~~~~~~~~~~~~~~~~~~~

The configuration specification for the Crash Test Dummy.

::

    crash_configspec = """
    plugin = option('CrashTestDummy')
    
    error_module = string(default='exceptions')
    error = string(default='Exception')
    error_message = string(default='My work is done, why wait?')
    function = string(default='__call__')
    """
    



CrashTestDummyConfiguration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A class to handle the config_obj configuration.

.. uml::

   BaseConfiguration <|-- CrashTestDummyConfiguration

.. autosummary::
   :toctree: api

   CrashTestDummyConfiguration
   CrashTestDummyConfiguration.configspec
   CrashTestDummyConfiguration.configuration
   CrashTestDummyConfiguration.product



CrashTestDummy
~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api

   CrashTestDummy
   


Stuck Dummy
-----------

The Configspec
~~~~~~~~~~~~~~

The configuration specification for the StuckDummy.

::

    stuck_dummy_configspec = """
    plugin = option('StuckDummy)
    
    __many__ = string
    """
    



Stuck Dummy Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

.. uml::

   BaseConfiguration <|-- StuckDummyConfiguration

.. autosummary::
   :toctree: api

   StuckDummyConfiguration
   StuckDummyConfiguration.configspec
   StuckDummyConfiguration.configuration
   StuckDummyConfiguration.product



Stuck Dummy
~~~~~~~~~~~

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

