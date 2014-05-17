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
    
    



The CheckArguments Class
------------------------

.. uml::

   BaseArguments <|-- CheckArguments

.. currentmodule:: ape.interface.arguments.checkarguments
.. autosummary::
   :toctree: api

   CheckArguments
   CheckArguments.configfiles
   CheckArguments.modules
   CheckArguments.reset
   CheckArguments.function

