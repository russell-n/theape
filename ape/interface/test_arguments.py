
# python standard library
import unittest
import random
import argparse

# third-party
from mock import MagicMock, patch

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
                             ['ape*.ini'],
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
                             ['ape*.ini'],
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

