The BaseStrategy
================

.. module:: theape.infrastructure.arguments.basestrategy






.. _ape-interface-arguments-base-strategy:

The BaseStrategy
----------------

This is a holder of sub-commands for the arguments. Its main purpose is to  provide the QuarterMaster and Ape-plugin, since one or both is being used by various sub-commands.

.. _ape-interface-arguments-basestrategy-class-model:

Class Model
-----------

.. uml::

   BaseStrategy o- QuarterMaster
   BaseStrategy o- TheApe
   BaseStrategy --|> BaseClass




.. _ape-interface-arguments-basestrategy-errors:

The Errors
----------

There are two kinds of exceptions caught which produce two error-messages:

.. csv-table:: Error Messages
   :header: Exception, Message, Meaning
   :delim: ;

   Exception; APE Error; Something unexpected happened -- this indicates a problem with the code
   KeyboardInterrupt; Oh, I am slain; User killed the runtime for some reason -- clean-up and then close




.. _ubootkommandant-api:

The API
-------

The decorator (:ref:`try_except <try-except-decorator>`) around most of these methods is blocking the docstrings. Follow the links to the source code to see what they do.

.. autosummary::
   :toctree: api

   UbootKommandant
   UbootKommandant.handle_help
   UbootKommandant.run
   UbootKommandant.fetch
   UbootKommandant.list_plugins
   UbootKommandant.check
   UbootKommandant.clean_up

Supporting Code
---------------

These are used within the UbootKommandant.

    * :ref:`The Base Class <ape-baseclass-baseclass>`
    * :ref:`The try-except Decorator <ape-commoncode-try-except-decorator>`
    * :ref:`The crash_handler log_error function <ape-commoncode-crash-handler-log-error>`
    * :ref:`The QuarterMaster <ape-plugins-quartemaster>`
    * :ref:`The Ape Plugin <apeplugin-introduction>`
