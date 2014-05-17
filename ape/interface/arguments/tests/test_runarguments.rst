Testing The RunArguments
========================

This tests the arguments for the `run` sub-command.

.. currentmodule:: ape.interface.arguments.arguments.tests.test_runarguments
.. autosummary::
   :toctree: api

   TestRunArguments.test_constructor
   TestRunArguments.test_configfiles
   TestRunArguments.test_function

::

    class TestRunArguments(unittest.TestCase):
        def setUp(self):
            self.args = ['run']
            self.arguments = RunArguments(args=self.args)
            return
        
        def test_constructor(self):
            """
            Does it build properly?
            """
            arguments = RunArguments(args='run')
            self.assertIsInstance(arguments, BaseArguments)
            # test the inheritance
            self.assertFalse(arguments.debug)
            return
    
        def test_configfiles(self):
            """
            Does it get the configfiles list?
            """
            # test default
            self.assertEqual(self.arguments.configfiles, RunArgumentsConstants.
    default_configfiles)
    
            #test arguments
            self.arguments.reset()
            configfiles =  'ape.ini cow.txt pie.bla'.split()
            self.arguments.args = self.args + configfiles
            self.assertEqual(self.arguments.configfiles, configfiles)
            return
    
        def test_function(self):
            """
            Does the arguments have the `run` strategy?
            """
            self.assertEqual(self.arguments.function, UbootKommandant.run)
            return
    
    

