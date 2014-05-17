Testing the ArgumentBuilder
===========================

.. currentmodule:: ape.interface.arguments.tests.test_argumentbuilder
.. autosummary:: api

   TestArgumentBuilder.test_constructor
   TestArgumentBuilder.test_parse_args

::

    # python standard library
    import unittest
    
    # the ape
    from ape.interface.arguments.argumentbuilder import ArgumentBuilder
    from ape.interface.arguments.fetcharguments import FetchArguments
    from ape.interface.arguments.runarguments import RunArguments
    from ape.interface.arguments.listarguments import ListArguments
    from ape.interface.arguments.checkarguments import CheckArguments
    from ape.interface.arguments.helparguments import HelpArguments
    
    

::

    class TestArgumentBuilder(unittest.TestCase):
        def test_constructor(self):
            """
            Does it build?
            """
            builder = ArgumentBuilder(args=['fetch'])
            return
    
        def test_parse_args(self):
            """
            Does it work like argparse?
            """
            builder = ArgumentBuilder(args=['fetch'])
            args = builder()
            self.assertEqual(args.command, 'fetch')
            self.assertIsInstance(args, FetchArguments)
    
            builder.args = ['run']
            args = builder()
            self.assertIsInstance(args, RunArguments)
    
            builder.args = ['list']
            args = builder()
            self.assertIsInstance(args, ListArguments)
    
            builder.args = ['check']
            args = builder()
            self.assertIsInstance(args, CheckArguments)
    
            builder.args = ['help']
            args = builder()
            self.assertIsInstance(args, HelpArguments)
            return
    
    

