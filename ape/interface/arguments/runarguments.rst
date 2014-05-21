The Run Sub-Command Arguments
=============================
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

Contents:

    * :ref:`Run Arguments Constants <ape-interface-run-arguments-constants>`
    * :ref:`Run Arguments Class <ape-interface-run-arguments-class>`
    * :ref:`Run Strategy <ape-interface-run-strategy>`



.. _ape-interface-run-arguments-constants:

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
    
    



.. _ape-interface-run-arguments-class:

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



.. _ape-interface-run-strategy:

The Run Strategy
----------------

This is the strategy for the `run` sub-command than runs the APE.

.. uml::

   BaseStrategy <|-- RunStrategy

.. autosummary::
   :toctree: api

   RunStrategy

