Testing the ArgumentClinic
==========================

This proved to require more work than I wanted to spend so it is largely incomplete.

::

    # python standard library
    import unittest
    import random
    import argparse
    
    # third-party
    try:
        from mock import MagicMock, patch
    except ImportError:
        pass
    
    # this package
    from ape.interface.arguments.arguments import ArgumentClinic
    



Testing the BaseArguments
-------------------------

This is to test the new docopt-based tests.

.. currentmodule:: ape.interface.test.test_arguments
.. autosummary::
   :toctree: api

   TestBaseArguments.test_constructor
   TestBaseArguments.test_debug
   TestBaseArguments.test_silent
   TestBaseArguments.test_pudb
   TestBaseArguments.test_pdb
   TestBaseArguments.test_trace
   TestBaseArguments.test_callgraph
   TestBaseArguments.test_version
   TestBaseArguments.test_options_first
   TestBaseArguments.test_command
   TestBaseArguments.test_subcommands

