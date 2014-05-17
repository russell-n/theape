Testing The Fetch Arguments
===========================

::

    # python standard library
    import unittest
    
    # the ape
    from ape.interface.arguments.fetcharguments import FetchArguments
    import ape.interface.arguments.fetcharguments
    
    



.. currentmodule:: ape.interface.arguments.tests.test_fetcharguments
.. autosummary::
   :toctree: api

   TestFetchArguments.test_constructor
   TestFetchArguments.test_names
   TestFetchArguments.test_modules
   TestFetchArguments.test_both

::

    fetch_usage = ape.interface.arguments.fetcharguments.__doc__
    class TestFetchArguments(unittest.TestCase):
        def setUp(self):
            self.args = ['fetch']
            self.arguments = FetchArguments(args=self.args)
            return
        
        def test_constructor(self):
            """
            Does it build?
            """
            arguments = FetchArguments(args=['fetch'])
    
            # test inheritance
            self.assertFalse(arguments.debug)
            self.assertEqual(fetch_usage, arguments.sub_usage)
            return
    
        def test_names(self):
            """
            Does it get the list of plugin names?
            """
            # default
            self.assertEqual(['Ape'], self.arguments.names)
    
            # positionl arguments
            self.arguments.reset()
            names = "apple banana cat".split()
            self.arguments.args = self.args + names
            self.assertEqual(names, self.arguments.names)
            return
    
        def test_modules(self):
            """
            Does it get a list of external modules?
            """
            # default is None
            self.assertEqual([], self.arguments.modules)
    
            # add one
            self.arguments.reset()
            modules = ['aoeu']
            options = ['-m'] + modules
            self.arguments.args = self.args + options
            self.assertEqual(modules, self.arguments.modules)
    
            # add multiple
            self.arguments.reset()
            modules = 'a b c d e'.split()
            options = ['-m'] + " -m".join(modules).split()
            self.arguments.args = self.args + options
            self.assertEqual(modules, self.arguments.modules)
            return
    
        def test_both(self):
            """
            Can you use both names and modules?
            """
            names = 'ab cd'.split()
            modules = 'a b c d'.split()
            arguments_options = names + ['-m'] + ' -m'.join(modules).split()
            self.arguments.args = self.args + arguments_options
            self.assertEqual(names, self.arguments.names)
            self.assertEqual(modules, self.arguments.modules)
            return
    # end TestFetchArguments    
    
    

