The Argument Clinic
===================
::

    """APE (the all-purpose-evaluator)
    
    Usage: ape -h | -v
           ape [--debug|--silent] [--pudb|--pdb] <command> [<argument>...]
           ape [--debug|--silent] [--trace|--callgraph] <command> [<argument>...]
    
    Help Options:
    
        -h, --help     Display this help message and quit.
        -v, --version  Display the version number and quit.
        
    Logging Options:
    
        --debug   Set logging level to DEBUG.
        --silent  Set logging level to ERROR.
    
    Debugging Options:
    
        --pudb       Enable the `pudb` debugger (if installed)
        --pdb        Enable the `pdb` (python's default) debugger
        --trace      Enable code-tracing
        --callgraph  Create a call-graph of for the code
    
    Positional Arguments:
    
        <command>      The name of a sub-command (see below)
        <argument>...  One or more options or arguments for the sub-command
        
    Available Sub-Commands:
    
        run    Run a plugin
        fetch  Fetch a sample configuration-file
        help   Display more help
        list   List known plugins
        check  Check a configuration
    
    To get help for a sub-command pass `-h` as the argument. e.g.:
    
        ape run -h
    
    """     
    


.. currentmodule:: ape.interface.arguments


Contents:

   * :ref:`The Argument Clinic <ape-interface-arguments-argument-clinic>`
   * :ref:`The Argument Constants <ape-interface-arguments-argumentconstants>`
   * :ref:`The BaseArguments <ape-interface-arguments-basearguments>`

.. _ape-interface-arguments-argument-clinic:

The Argument Clinic
-------------------

.. _argument-clinic:

This is the module that builds the command-line interface for the Ape. It uses the python `argparse <http://docs.python.org/2/library/argparse.html>`_ module. In particular it uses the :ref:`UbootKommandant <uboot-kommandant>` to provide methods for the ArgParser's `sub-command <http://docs.python.org/2.7/library/argparse.html#sub-commands>`_ interface.

.. superfluous '

.. uml::

   ArgumentClinic o- argparse.ArgumentParser
   ArgumentClinic o- UbootKommandant

.. autosummary::
   :toctree: api

   ArgumentClinic
   ArgumentClinic.args
   ArgumentClinic.__call__
   ArgumentClinic.add_arguments
   ArgumentClinic.add_subparsers

The ArgumentClinic uses sub-parsers to enable the use of :ref:`sub-commands <untersee-boot>`.




This is what the ``--help`` flag gives as of October 17, 2013 (Pweave hijacks the ArgumentParser so an example has to be generated separately):

.. literalinclude:: sample_help.txt

.. _ape-interface-arguments-argumentconstants:

The ArgumentConstants
---------------------

::

    class ArgumentsConstants(object):
        """
        Constants for the arguments
        """
        __slots__ = ()
        debug = "--debug"
        silent = '--silent'
        pudb = "--pudb"
        pdb = '--pdb'
        trace = '--trace'
        callgraph = '--callgraph'
        command = "<command>"
        argument = '<argument>'
    # end ArgumentConstants    
    
    



.. _ape-interface-arguments-basearguments:

The BaseArguments
-----------------

This is the base-class for the newer docopt-based arguments. See the :ref:`developer documentation <docopt-reproducingape-ape-usage-string>` for a more detailed explanation of what's going on.

.. currentmodule:: docopt
.. autosummary::
   :toctree: api

   docopt
   DocoptExit

.. '

.. uml::

   BaseClass <|-- BaseArguments
   BaseArguments o-- CheckArguments
   BaseArguments o-- RunArguments
   BaseArguments o-- FetchArguments
   BaseArguments o-- ListArguments
   BaseArguments o-- HelpArguments

.. currentmodule:: ape.interface.arguments.arguments
.. autosummary::
   :toctree: api

   BaseArguments
   BaseArguments.arguments
   BaseArguments.sub_arguments
   BaseArguments.debug
   BaseArguments.silent
   BaseArguments.pudb
   BaseArguments.pdb
   BaseArguments.trace
   BaseArguments.callgraph
   BaseArguments.reset

