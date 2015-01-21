The Check Sub-Command Arguments
===============================

.. code:: python

    """`check` sub-command
    
    usage: ape check -h
           ape check  [<config-file-name> ...] [--module <module> ...]
    
    Positional Arguments:
    
        <config-file-name> ...    List of config files (e.g. *.ini -
    default='['ape.ini']')
    
    optional arguments:
    
        -h, --help                  Show this help message and exit
        -m, --module <module>       Non-ape module with plugins
    
    """
    



See the :ref:`developer documentation <docopt-reproducingape-check-sub-command>` for more information about this.




.. _ape-interface-arguments-check-arguments-constants:

The CheckArgumentsConstants
---------------------------


.. code:: python

    class CheckArgumentsConstants(object):
        """
        A holder of constants for the Check Sub-Command Arguments
        """
        __slots__ = ()
        # options and arguments
        configfilenames = "<config-file-name>"
        modules = "--module"
    
        #defaults
        default_configfilenames = ['ape.ini']
    



.. _ape-interface-arguments-check-arguments-class:

The Check Class
---------------

.. uml::

   BaseArguments <|-- Check

.. module:: theape.interface.arguments.checkarguments
.. autosummary::
   :toctree: api

   Check
   Check.configfiles
   Check.modules
   Check.reset
   Check.function




.. _ape-interface-arguments-check-strategy:

The Check Strategy
------------------

The Check strategy calls `check_rep` on the plugins.

.. uml::

   BaseStrategy <|-- CheckStrategy

.. autosummary::
   :toctree: api

   CheckStrategy
   CheckStrategy.function




