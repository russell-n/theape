Testing the Dummy Plugin
========================

The `Dummy` plugin inherits from the :ref:`BasePlugin <base-plugin>` and so takes two parameters on instantiation:

   * configuration (a configuration map to get config-file values from)

   * section_header (the section name that has values for the plugin)

The section parameter `section_header` was added so that more than one configuration of each plugin can be used. Since the operator is passing this in to all  the plugins it can be assumed that it will always exist (in the current implementation of the ape).

.. module:: theape.plugins.tests.test_dumy_pluing

.. autosummary::
   :toctree: api

   TestingDummyPlugin.test_constructor
   TestingDummyPlugin.test_product



   









