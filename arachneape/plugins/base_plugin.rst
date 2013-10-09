The Base Plugin
===============
.. currentmodule:: arachneape.plugins.base_plugin

.. _base-plugin:
In order to make the plugins a little more predictable they should inherit their interface from this (abstract) base-class.

.. uml::

   BasePlugin -|> BaseClass

.. autosummary::
   :toctree: api

   BasePlugin
   BasePlugin.help
   BasePlugin.product
   BasePlugin.config
   BasePlugin.author

