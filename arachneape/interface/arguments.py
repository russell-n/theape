
# python standard library
import argparse

# this package
from ubootkommandant import UbootKommandant


class ArgumentClinic(object):
    """
    A command-line argument parser
    """
    def __init__(self):
        """
        The ArgumentClinic Constructor
        """
        self._subcommand = None
        self._parser = None        
        self._subparsers = None
        self._args = None
        return

    @property
    def subcommand(self):
        """
        The sub-command strategies for the sub-parsers
        """
        if self._subcommand is None:
            self._subcommand = UbootKommandant()
        return self._subcommand        

    @property
    def subparsers(self):
        """
        sub-parsers for the parser
        """
        if self._subparsers is None:
            self._subparsers = self.parser.add_subparsers(title='Sub-Commands Help',
                                                          description='Available Subcommands',
                                                          help="SubCommands")
        return self._subparsers

    @property
    def parser(self):
        """
        An ArgumentParser
        """
        if self._parser is None:
            self._parser = argparse.ArgumentParser(prog=__package__)            
        return self._parser

    def add_arguments(self):
        """
        Adds the arguments to the parser
        """
        self.parser.add_argument('--debug',
                                 help='Sets the logging level to debug',
                                 action='store_true',
                                 default=False)
        self.parser.add_argument('--silent',
                                 help='Sets the logging level to off (for stdout)',
                                 action='store_true',
                                 default=False)
        self.parser.add_argument('--pudb',
                                  help='Enables the pudb debugger',
                                  action='store_true',
                                  default=False)
        self.parser.add_argument('--pdb',
                                help='Enables the pdb debugger',
                                action='store_true',
                                default=False)
        return
    
    def add_subparsers(self):
        """
        Adds subparsers to the parser

        I am now adding these to self so that the sub-parsers are public
        """
        self.runner = self.subparsers.add_parser("run",
                                                 help="Run the ArachneApe")
        self.runner.add_argument("configfiles",
                                 help="A list of config file name (default='%(default)s').",
                                 metavar="<config-file list>",
                                 default=["arachneape.ini"],
                                 nargs="*")
        self.runner.set_defaults(function=self.subcommand.run)

        self.fetcher = self.subparsers.add_parser("fetch",
                                                  help="Fetch a sample config file.")
        self.fetcher.add_argument('names',
                                  help="List of plugin-names (default=%(default)s)",
                                  default=["ArachneApe"],
                                  nargs="*")
        self.fetcher.set_defaults(function=self.subcommand.fetch)

        self.lister = self.subparsers.add_parser("list",
                                                 help="List available plugins.")
        self.lister.set_defaults(function=self.subcommand.list_plugins)

        self.checker = self.subparsers.add_parser('check',
                                                  help='Check your setup.')
        self.checker.add_argument("configfiles",
                                  help="List of config files (e.g. *.ini - default='%(default)s').",
                                  metavar="<config-file list>",
                                  default=["arachneape.ini"],
                                  nargs="*")

        self.checker.set_defaults(function=self.subcommand.check)

        self.helper = self.subparsers.add_parser("help",
                                                 help="Show more help")
        self.helper.add_argument('name',
                                 help="A specific plugin to inquire about.",
                                 nargs="?", default='ArachneApe')
        self.helper.add_argument('-w', '--width',
                                 help="Number of characters to wide to format the page.",
                                 type=int, default=70)

        self.helper.set_defaults(function=self.subcommand.handle_help)
        return
    
    @property
    def args(self):
        """
        The parsed args (adds arguments and sub-commands first)
        """
        if self._args is None:
            self.add_arguments()
            self.add_subparsers()
            self._args =  self.parser.parse_args()
        return self._args

    def __call__(self):
        """
        The main interface

        :return: argparse namespace
        """
        return self.args
# end class ArgumentClinic        


# python standard library
import unittest
import random

# third-party
from mock import MagicMock, patch


class TestArgumentClinic(unittest.TestCase):
    def setUp(self):
        self.keys = 'debug silent pudb pdb'.split()
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
                             ['arachneape.ini'],
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
                             ['ArachneApe'],
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
                             ['arachneape.ini'],
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
                             'ArachneApe',
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

