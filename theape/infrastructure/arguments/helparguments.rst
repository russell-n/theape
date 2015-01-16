The Help Sub-Command Arguments
==============================

.. code:: python

    """`help` sub-command
    
    usage: ape help -h
           ape help [-w WIDTH] [--module <module>...] [<name>]
    
    positional arguments:
        <name>                A specific plugin to inquire about [default: Ape].
    
    optional arguments:
        -h, --help            show this help message and exit
        -w , --width <width>  Number of characters to wide to format the page. [default: 80]
        -m, --module <module>     non-ape module with plugins
        
    """






.. _ape-interface-arguments-help-constants:

The Help Arguments Constants
----------------------------

.. module:: theape.interface.arguments.helparguments
.. autosummary::
   :toctree: api

   HelpArgumentsConstants




.. _ape-interface-help-arguments-class:

The Help Class
--------------

.. uml::

   BaseArguments <|-- Help

.. autosummary::
   :toctree: api

   Help
   Help.width
   Help.modules
   Help.reset
   Help.name
   Help.function




.. _ape-interface-arguments-help-strategy:

The Help Strategy
-----------------

.. uml::

   BaseStrategy <|-- HelpStrategy

.. autosummary::
   :toctree: api

   HelpStrategy
   HelpStrategy.function



