The ArachneApe Plugin
=====================

This is a default plugin to provide the base-level of features. This allows the code to have a fall-back when the user does not specify a plugin. The use of the word `plugin` in the module name seems redundant, but I am trying to avoid namespace problems since the base package is named ``arachneape``.



.. uml::

   ArachneApe -|> BasePlugin

.. autosummary::

   ArachneApe
   ArachneApe.help
   ArachneApe.product
   ArachneApe.config

