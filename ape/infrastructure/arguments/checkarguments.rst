The Check Sub-Command Arguments
===============================
::

    """`check` sub-command
    
    usage: ape check -h
           ape check  [<config-file-name> ...] [--module <module> ...]
    
    Positional Arguments:
    
        <config-file-name> ...    List of config files (e.g. *.ini - default='[
    'ape.ini']')
    
    optional arguments:
    
        -h, --help                  Show this help message and exit
        -m, --module <module>       Non-ape module with plugins
    
    """
    
    



See the :ref:`developer documentation <docopt-reproducingape-check-sub-command>` for more information about this.

Contents:

   * :ref:`Check Arguments Constants <ape-interface-arguments-check-arguments-constants>`
   * :ref:`Check Arguments Class <ape-interface-arguments-check-arguments-class>`
   * :ref:`Check Strategy <ape-interface-arguments-check-strategy>`



.. _ape-interface-arguments-check-arguments-constants:

The CheckArgumentsConstants
---------------------------

::

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

.. currentmodule:: ape.interface.arguments.checkarguments
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

