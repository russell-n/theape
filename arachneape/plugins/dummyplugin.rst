The Dummy Plugin
================

.. _dummy-plugin:
The :ref:`DummyClass <dummy-class>` does not do anything. It is meant to be used to test the infrastructure.



.. uml::

   DummyPlugin -|> BasePlugin
   DummyPlugin o- HelpPage

.. autosummary::
   :toctree: api

   DummyPlugin
   DummyPlugin.help
   DummyPlugin.product
   DummyPlugin.config

