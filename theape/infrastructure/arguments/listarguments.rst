The List Sub-Command Arguments
==============================

.. code:: python

    """list subcommand
    
    usage: ape list -h
           ape list [<module> ...]
    
    Positional Arguments:
      <module> ...  Space-separated list of importable module with plugins
    
    optional arguments:
    
      -h, --help                 Show this help message and exit
    
    """



See the :ref:`developer documentation <docopt-reproducingape-list-sub-command>` for more information.




.. _ape-interface-arguments-list-arguments-constants:

The ListArguments Constants
---------------------------


.. code:: python

    class ListArgumentsConstants(object):
        """
        Constants for the list sub-command arguments
        """
        __slots__ = ()
        # arguments
        modules = "<module>"
    



.. _ape-interface-arguments-list-arguments-class:

The List Class
--------------

.. uml::

   BaseArguments <|-- List

.. module:: theape].interface.arguments.listarguments
.. autosummary::
   :toctree: api

   List
   List.modules
   List.reset
   List.function





.. _ape-interface-arguments-list-strategy:

The List Strategy
-----------------

.. uml::

   BaseStrategy <|-- ListStrategy

.. module:: theape.interface.arguments.listarguments
.. autosummary::
   :toctree: api

   ListStrategy
   ListStrategy.function




