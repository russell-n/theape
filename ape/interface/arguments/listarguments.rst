The List Sub-Command Arguments
==============================
::

    """list subcommand
    
    usage: ape list -h
           ape list [<module> ...]
    
    Positional Arguments:
      <module> ...  Space-separated list of importable module with plugins
    
    optional arguments:
    
      -h, --help                 Show this help message and exit
    
    """
    



See the :ref:`developer documentation <docopt-reproducingape-list-sub-command>` for more information.

Contents:

    * :ref:`The List Arguments Constants <ape-interface-arguments-list-arguments-constants>`
    * :ref:`The List Arguments Class <ape-interface-arguments-list-arguments-class>`
    * :ref:`The List Strategy <ape-interface-arguments-list-strategy>`



.. _ape-interface-arguments-list-arguments-constants:

The ListArguments Constants
---------------------------

::

    class ListArgumentsConstants(object):
        """
        Constants for the list sub-command arguments
        """
        __slots__ = ()
        # arguments
        modules = "<module>"
    
    



.. _ape-interface-arguments-list-arguments-class:

The ListArguments Class
-----------------------

.. uml::

   BaseArguments <|-- ListArguments

.. currentmodule:: ape.interface.arguments.listarguments
.. autosummary::
   :toctree: api

   ListArguments
   ListArguments.modules
   ListArguments.reset
   ListArguments.function




.. _ape-interface-arguments-list-strategy:

The List Strategy
-----------------

.. uml::

   BaseStrategy <|-- ListStrategy

.. currentmodule:: ape.interface.arguments.listarguments
.. autosummary::
   :toctree: api

   ListStrategy
   ListStrategy.function

