The Fetch Sub-Command Arguments
===============================
::

    """fetch subcommand
        
    usage: ape fetch -h
           ape fetch [<name>...]  [--module <module> ...] 
    
    positional arguments:
        <name>                         List of plugin-names (default=['Ape'])
    
    optional arguments:
        -h, --help                     Show this help message and exit
        -m, --module <module> ...      Non-ape modules
    """
    
    



These are arguments for the `fetch` sub-command (see the :ref:`developer documentation <docopt-reproducingape-fetch-sub-command>` for more information).



The Fetch Arguments Constants
-----------------------------

::

    class FetchArgumentsConstants(object):
        """
        Constants for the `fetch` sub-command arguments
        """    
        __slots__ = ()
        # arguments and options
        names = "<name>"
        modules = '--module'
        
        # defaults
        default_names = ['Ape']
    
    



The FetchArguments
------------------

.. uml::

   BaseArguments <|-- FetchArguments

.. currentmodule:: ape.interface.arguments.fetcharguments
.. autosummary::
   :toctree: api

   FetchArguments
   FetchArguments.names
   FetchArguments.modules
   FetchArguments.reset



The FetchStrategy
-----------------

.. autosummary::
   :toctree: api

   FetchStrategy
   FetchStrategy.function



The `function` method is wrapped by the :ref:`try_except decorator <ape-commoncode-try-except-decorator>` so it should never crash.
