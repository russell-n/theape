
# python standard library
import unittest

# the APE
from ape.interface.arguments.arguments import BaseArguments
from ape.interface.arguments.checkarguments import CheckArguments

class TestCheckArguments(unittest.TestCase):
    def setUp(self):
        self.args = ['check']
        self.arguments = CheckArguments(args=self.args)
        return
    
    def test_constructor(self):
        """
        Does it build?
        """
        arguments = CheckArguments()
        self.assertIsInstance(arguments, BaseArguments)

        # check that the parent is being instantiated
        arguments.args = '--debug check'.split()
        self.assertTrue(arguments.debug)
        return

    def test_configfilenames(self):
        """
        Does it get the list of config-files?
        """
        default = ['ape.ini']
        self.assertEqual(self.arguments.configfiles, default)

        self.arguments.reset()
        filenames = "umma gumma".split()
        self.arguments.args = self.args + filenames
        self.assertEqual(self.arguments.configfiles, filenames)
        return

    def test_modules(self):
        """
        Does it get a list of optional module names?
        """
        self.assertEqual([], self.arguments.modules)

        self.arguments.reset()
        self.arguments.args = self.args + '--module cow -m man'.split()
        self.assertEqual(self.arguments.modules, 'cow man'.split())
        return

    def test_both(self):
        """
        Does it work if you combine modules and config file names?
        """
        self.arguments.args = "check -m big.pig dog war".split()
        self.assertEqual('dog war'.split(), self.arguments.configfiles)
        self.assertEqual(["big.pig"], self.arguments.modules)
        return
# end TestCheckArguments    
