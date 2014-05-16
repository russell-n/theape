
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
from ape.interface.arguments import ArgumentClinic


class TestArgumentClinic(unittest.TestCase):
    def setUp(self):
        self.keys = 'debug silent pudb pdb trace callgraph'.split()
        self.flags = ["--{0}".format(key) for key in self.keys]

        self.args = MagicMock(spec='sys')
        self.parser = MagicMock(name='ArgumentParser', spec=argparse.ArgumentParser)
        self.subcommander = MagicMock(name='UbootKommandant')
        self.argparse = MagicMock(name='argparse')
        self.argparse.return_value = self.parser

        self.clinic = ArgumentClinic()
        self.clinic._subcommand = self.subcommander
        return

    def test_parser(self):
        """
        Does it have an argparse.ArgumentParser as its parser?
        """
        with patch('argparse.ArgumentParser',
                                      self.argparse):
            parser = self.clinic.parser
        self.assertEqual(parser, self.parser)
        return

    def test_add_argumentS(self):
        """
        Does it add the right arguments?
        """
        # add_arguments can only be called once or it will raise an error
        self.clinic.add_arguments()
        args = MagicMock()
        
        # first the defaults are checked
        argv = 'command'.split()

        def getitem(index):
            return argv[index]

        args.__getitem__.side_effect = getitem
        with patch('sys.argv', args):
            namespace = self.clinic.parser.parse_args()
            
        for key in self.keys:
            self.assertFalse(getattr(namespace, key))

        # now turn them all on

        argv = ['command'] + self.flags
        args.__getitem__.side_effect = lambda index: argv[index]
        with patch('sys.argv', args):
            namespace = self.clinic.parser.parse_args()
        for key in self.keys:
            self.assertTrue(getattr(namespace, key))

        # are those the only arguments?
        self.assertEqual(sorted(self.keys), sorted(namespace.__dict__.keys()))
        return

    def subparser_check(self, argv, variable, expected, function_mock):
        self.clinic.add_subparsers()
        self.args.__getitem__.side_effect = lambda index: argv[index]
        with patch('sys.argv', self.args):
            namespace = self.clinic.parser.parse_args()
        self.assertTrue(hasattr(namespace, variable))
        self.assertEqual(getattr(namespace, variable), expected)
        self.assertEqual(namespace.function, function_mock)
        return
    
    def test_run_subparser(self):
        """
        Does it add the correct sub-parsers?
        """
        run_mock = MagicMock(name='run')
        self.subcommander.run = run_mock
        argv = 'command run a b c'.split()
        self.subparser_check(argv, 'configfiles', 'a b c'.split(),
                             run_mock)
        argv = 'command run'.split()
        self.subparser_check(argv, 'configfiles',
                             ['ape.ini'],
                             run_mock)
        
        return

    def test_fetch_subparser(self):
        fetch_mock = MagicMock(name='fetch')
        self.subcommander.fetch = fetch_mock
        argv = 'command fetch d e f'.split()
        self.subparser_check(argv, 'names', 'd e f'.split(),
                             fetch_mock)
        # default
        argv = 'command fetch'.split()
        self.subparser_check(argv, 'names',
                             ['Ape'],
                             fetch_mock)

        return

    def test_check_subparser(self):
        check_mock = MagicMock(name='check')
        self.subcommander.check = check_mock
        argv = 'command check g'.split()
        self.subparser_check(argv,
                             'configfiles',
                             ['g'],
                             check_mock)

        # default
        argv = 'command check'.split()
        self.subparser_check(argv,
                             'configfiles',
                             ['ape.ini'],
                             check_mock)

        return

    def test_help_subparser(self):
        help_mock = MagicMock(name='help')
        self.subcommander.handle_help = help_mock
        argv = 'command help me'.split()
        self.subparser_check(argv,
                             'name',
                             'me',
                             help_mock)
        argv = 'command help'.split()
        self.subparser_check(argv,
                             'name',
                             'Ape',
                             help_mock)
        return

    def test_list_subparser(self):
        list_mock = MagicMock(name='list')
        self.subcommander.list_plugins = list_mock

        self.clinic.add_subparsers()
        argv = 'command list'.split()
        self.args.__getitem__.side_effect = lambda index: argv[index]
        with patch('sys.argv', self.args):
            namespace = self.clinic.parser.parse_args()
        self.assertEqual(namespace.function, list_mock)
        return

    def test_call(self):
        command = ['command']
        option = random.choice(self.flags)



#third-party
import docopt

# this package
import ape.interface.arguments
from ape import BaseClass
from ape import VERSION

usage = ape.interface.arguments.__doc__

class TestBaseArguments(unittest.TestCase):
    def setUp(self):
        self.args = ['cow']
        self.arguments = ape.interface.arguments.BaseArguments(args=self.args)
        return
    
    def test_constructor(self):
        """
        Does it build?
        """
        arguments = ape.interface.arguments.BaseArguments()
        self.assertIsInstance(arguments, BaseClass)
        self.assertEqual(arguments.usage, usage)
        self.assertIsNone(arguments.args)
        return

    def test_debug(self):
        """
        Does it correctly set the debug value?
        """
        self.assertFalse(self.arguments.debug)
        self.arguments.reset()

        self.arguments.args = '--debug cow'.split()
        self.assertTrue(self.arguments.debug)

        # mutual exclusivity
        self.arguments.reset()
        self.arguments.args = '--debug --silent cow'.split()
        with self.assertRaises(docopt.DocoptExit):
            self.arguments.debug
        return

    def test_silent(self):
        """
        Does it set the silent option?
        """
        self.assertFalse(self.arguments.silent)

        self.arguments.reset()
        self.arguments.args = '--silent cow'.split()
        self.assertTrue(self.arguments.silent)

        # test mutual-exclusivity
        self.arguments.reset()
        with self.assertRaises(docopt.DocoptExit):
            self.arguments.args = '--silent --debug cow'.split()
            self.arguments.silent
        return

    def test_pudb(self):
        """
        Does it set the pudb option?
        """
        self.assertFalse(self.arguments.pudb)

        self.arguments.reset()
        self.arguments.args = '--pudb cow'.split()
        self.assertTrue(self.arguments.pudb)

        self.arguments.reset()
        self.arguments.args = "--pudb --pdb cow".split()
        with self.assertRaises(docopt.DocoptExit):
            self.arguments.pudb
        return

    def test_pdb(self):
        """
        Does it set the `pdb` option?
        """
        self.assertFalse(self.arguments.pdb)

        self.arguments.reset()
        self.arguments.args = '--pdb cow'.split()
        self.assertTrue(self.arguments.pdb)

        # mutually exclusive
        self.arguments.reset()
        self.arguments.args = '--pdb --pudb cow'.split()
        with self.assertRaises(docopt.DocoptExit):
            self.arguments.pdb           
        return

    def test_trace(self):
        """
        Does it set the trace flag?
        """
        self.assertFalse(self.arguments.trace)

        self.arguments.reset()
        self.arguments.args = '--trace  cow'.split()
        self.assertTrue(self.arguments.trace)

        self.arguments.reset()
        self.arguments.args = '--trace --callgraph cow'.split()
        with self.assertRaises(docopt.DocoptExit):
            self.arguments.trace
        return

    def test_callgraph(self):
        """
        Does it set the callgraph option?
        """
        self.assertFalse(self.arguments.callgraph)
        
        self.arguments.reset()
        self.arguments.args = "--callgraph cow".split()
        self.assertTrue(self.arguments.callgraph)

        self.arguments.reset()
        self.arguments.args = "--callgraph --trace cow".split()
        with self.assertRaises(docopt.DocoptExit):
            self.arguments.callgraph
        return

    def test_version(self):
        """
        Does it set the version?
        """
        mock_docopt = MagicMock()
        for option_first in (True, False):
            arguments = ape.interface.arguments.BaseArguments(options_first=option_first)    

            with patch('docopt.docopt', mock_docopt):
                arguments.debug
            mock_docopt.assert_called_with(doc=usage,
                                           argv=None,
                                           options_first=option_first,
                                           version=VERSION)
        
        
            mock_docopt.reset()
        return

    def test_options_first(self):
        """
        Is the default for options first True?
        """
        self.assertTrue(self.arguments.options_first)
        arguments = ape.interface.arguments.BaseArguments(options_first=False)
        self.assertFalse(arguments.options_first)
        return
# end class TestBaseArguments    


from ape.interface.checkarguments import CheckArguments

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
        self.assertIsInstance(arguments, ape.interface.arguments.BaseArguments)

        # check that the parent is being instantiated
        arguments.args = '--debug check'.split()
        self.assertTrue(arguments.debug)
        return

    def test_configfilenames(self):
        """
        Does it get the list of config-files?
        """
        default = ['ape.ini']
        self.assertEqual(self.arguments.configfilenames, default)

        self.arguments.reset()
        filenames = "umma gumma".split()
        self.arguments.args = self.args + filenames
        self.assertEqual(self.arguments.configfilenames, filenames)
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
        self.assertEqual('dog war'.split(), self.arguments.configfilenames)
        self.assertEqual(["big.pig"], self.arguments.modules)
        return
# end TestCheckArguments    
