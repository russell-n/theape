The Run Sub-Command Arguments
=============================

.. code:: python

    """`run` sub-command
    
    Usage: theape run -h
           theape run [<configuration>...]
    
    Positional Arguments:
    
        <configuration>   0 or more configuration-file names [default:
    ape.ini]
    
    Options;
    
        -h, --help  This help message.
    
    """
    



See the :ref:`developer documentation <docopt-reproducingape-run-sub-command>` for more information about this section.




.. _ape-interface-run-arguments-constants:

The RunArguments Constants
--------------------------


.. code:: python

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

.. module:: theape.interface.arguments.runarguments
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






