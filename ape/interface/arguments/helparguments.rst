The Help Sub-Command Arguments
==============================
::

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
    



The Help Arguments Constants
----------------------------

.. currentmodule:: ape.interface.arguments.helparguments
.. autosummary::
   :toctree: api

   HelpArgumentsConstants



The HelpArguments Class
-----------------------

.. uml::

   BaseArguments <|-- HelpArguments

.. autosummary::
   :toctree: api

   HelpArguments
   HelpArguments.width
   HelpArguments.modules
   HelpArguments.reset
   HelpArguments.name
   HelpArguments.function

