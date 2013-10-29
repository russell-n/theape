
# python standard library
import argparse

# this package
from ubootkommandant import UbootKommandant


document_this = __name__ == '__builtin__'


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
        self.parser.add_argument('--trace',
                                 help='Turn on code-tracing',
                                 action='store_true',
                                 default=False)

        self.parser.add_argument('--callgraph',
                                 help='Create call-graph',
                                 action='store_true',
                                 default=False)
        return
    
    def add_subparsers(self):
        """
        Adds subparsers to the parser

        I am now adding these to self so that the sub-parsers are public
        """
        self.runner = self.subparsers.add_parser("run",
                                                 help="Run the Ape")
        self.runner.add_argument("configfiles",
                                 help="A list of config file name (default='%(default)s').",
                                 metavar="<config-file list>",
                                 default=["ape.ini"],
                                 nargs="*")
        self.runner.set_defaults(function=self.subcommand.run)

        self.fetcher = self.subparsers.add_parser("fetch",
                                                  help="Fetch a sample config file.")
        self.fetcher.add_argument('names',
                                  help="List of plugin-names (default=%(default)s)",
                                  default=["Ape"],
                                  nargs="*")
        self.fetcher.add_argument('--modules',
                                help='Non-ape modules',
                                nargs='*')
        self.fetcher.set_defaults(function=self.subcommand.fetch)

        self.lister = self.subparsers.add_parser("list",
                                                 help="List available plugins.")
        self.lister.add_argument('--modules',
                                 help='Space-separated list of non-ape modules with plugins',
                                 nargs='*')
        self.lister.set_defaults(function=self.subcommand.list_plugins)

        self.checker = self.subparsers.add_parser('check',
                                                  help='Check your setup.')
        self.checker.add_argument("configfiles",
                                  help="List of config files (e.g. *.ini - default='%(default)s').",
                                  metavar="<config-file list>",
                                  default=["ape.ini"],
                                  nargs="*")
        self.checker.add_argument("--modules",
                                  help='Space-separated list of non-ape modules with plugins',
                                 nargs='*')

        self.checker.set_defaults(function=self.subcommand.check)

        self.helper = self.subparsers.add_parser("help",
                                                 help="Show more help")
        self.helper.add_argument('name',
                                 help="A specific plugin to inquire about.",
                                 nargs="?", default='Ape')
        self.helper.add_argument('-w', '--width',
                                 help="Number of characters to wide to format the page.",
                                 type=int, default=70)
        self.helper.add_argument('--modules',
                                 help='Space-separated list of non-ape modules with plugins',
                                 nargs='*')

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
