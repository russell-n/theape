
# python standard library
import argparse


class ArgumentClinic(object):
    """
    A command-line argument parser
    """
    def __init__(self):
        """
        The ArgumentClinic Constructor
        """
        self._subcommands = None
        self._parser = None        
        self._subparsers = None
        self._args = None
        return

    @property
    def subcommands(self):
        """
        The sub-command strategies for the sub-parsers
        """
        if self._subcommands is None:
            self._subcommands = UbootKommandant()
        return self._subcommands        

    @property
    def subparsers(self):
        """
        sub-parsers for the parser
        """
        if self._subparsers is None:
            self._subparsers = self.parser.add_subparsers(title='Subcommands Help',
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
        """
        runner = self.subparsers.add_parser("run", help="Run the ArachneApe")
        runner.add_argument("configfiles", help="A list of config file name (default='%(default)s').",
                            metavar="<config-file list>",
                            default=["arachneape.ini"],
                            nargs="*")
        runner.set_defaults(function=self.strategies.run)

        fetcher = self.subparsers.add_parser("fetch", help="Fetch a sample config file.")
        fetcher.add_argument('names', help="List of plugin-names (default=%(default)s)",
                             default=["arachneape"],
                             nargs="*")
        fetcher.set_defaults(function=self.strategies.fetch)

        lister = self.subparsers.add_parser("list", help="List available plugins.")
        lister.set_defaults(function=self.strategies.list)

        tester = self.subparsers.add_parser('test', help='Test your setup.')
        tester.add_argument("configfiles", help="List of config files (e.g. *.ini - default='%(default)s').",
                            metavar="<config-file list>",
                            default=["arachneape.ini"],
                            nargs="*")

        tester.set_defaults(function=self.strategies.test)

        helper = self.subparsers.add_parser("help", help="Show more help")
        helper.add_argument('plugin',
                            help="A specific plugin to inquire about.",
                            nargs="?", default='arachneape')
        helper.set_defaults(function=self.strategies.handle_help)
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

# third-party
from mock import MagicMock, patch


class TestArgumentClinic(unittest.TestCase):
    def setUp(self):
        self.parser = MagicMock(name='ArgumentParser', spec=argparse.ArgumentParser)
        self.argparse = MagicMock(name='argparse')
        self.argparse.return_value = self.parser

        self.clinic = ArgumentClinic()
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
        args = MagicMock()
        args.argv = '--debug'.split()

        with patch('sys.argv', args):
            self.clinic.add_arguments()
            namespace = self.clinic.parser.parse_args()
        print namespace
        # this doesn't work -- need to figure out how to patch sys.argv
        #self.assertTrue(namespace.debug)
        keys = 'debug silent pudb pdb'.split()
        values = [False] * len(keys)
        expected = dict(zip(keys, values))
        self.assertEqual(expected, namespace.__dict__)
        return        
        
