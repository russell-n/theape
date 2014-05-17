The Run Arguments
=================
::

    """`run` sub-command
    
    Usage: ape run -h
           ape run [<configuration>...]
    
    Positional Arguments:
    
        <configuration>   0 or more configuration-file names [default: ape.ini]
    
    
    Options;
    
        -h, --help  This help message.
    
    """
    
    



See the :ref:`developer documentation <docopt-reproducingape-run-sub-command>` for more information about this section.



The RunArguments Constants
--------------------------

::

    class RunArgumentsConstants(object):
        """
        Constants for the Run Arguments
        """
        __slots__ = ()
        configfiles = '<configuration>'
        
        # defaults
        default_configfiles = ['ape.ini']
    # RunArgumentsConstants    
    
    




The RunArguments Class
----------------------

.. uml::

   BaseArguments <|-- RunArguments

.. currentmodule:: ape.interface.arguments.runarguments
.. autosummary::
   :toctree: api

   RunArguments
   RunArguments.configfiles
   RunArguments.reset

