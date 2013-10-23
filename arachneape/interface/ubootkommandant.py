
# third-party
from pycallgraph import PyCallGraph
from pycallgraph import GlobbingFilter
from pycallgraph import Config
from pycallgraph.output import GraphvizOutput

# this package
from arachneape.commoncode.baseclass import BaseClass
from arachneape.commoncode.crash_handler import try_except
from arachneape.commoncode.strings import RED, BOLD, RESET
from arachneape.plugins.quartermaster import QuarterMaster


class UbootKommandant(BaseClass):
    """
    a subcommand holder
    """
    def __init__(self):
        """
        UbootKommandant Constructor
        """
        super(UbootKommandant, self).__init__()
        self._quartermaster = None
        self.error = Exception
        self.error_message = "Oops, I Crapped My Pants"
        return

    @property
    def quartermaster(self):
        """
        A quartermaster for the plugins
        """
        if self._quartermaster is None:
            self._quartermaster = QuarterMaster()
        return self._quartermaster

    @try_except
    def list_plugins(self, args):
        """
        Calls the QuarterMaster and lists plugins

        :param:

         - `args`: not used
        """
        self.quartermaster.list_plugins()
        return

    @try_except
    def run(self, args):
        """
        Builds and runs the code
        """
        plugin = self.quartermaster.get_plugin('ArachneApe')

        # The arachneape needs the config-filenames
        ape = plugin(configfiles=args.configfiles).product
        if args.trace:
            from trace import Trace
        
            tracer = Trace(trace=True,
                           ignoremods= ['__init__', 'handlers',
                                        'threading', 'genericpath',
                                        'posixpath'],
                           timing=True)
            tracer.runfunc(ape)
        elif args.callgraph:
            config = Config(max_depth=10)
            graphviz = GraphvizOutput()
            graphviz.output_file = 'arachneape_callgraph.png'
            with PyCallGraph(output=graphviz, config=config):
                ape()
        else:
            ape()
        return

    @try_except
    def fetch(self, args):
        """
        'fetch' a sample plugin config-file

        :param:

         - `args`: namespace with 'names' list attribute
        """
        for name in args.names:
            self.logger.debug("Getting Plugin: {0}".format(name))
            plugin = self.quartermaster.get_plugin(name)
            # the quartermaster returns definitions, not instances
            plugin().fetch_config()
        return

    @try_except
    def check(self, args):
        """
        Builds and checks the configuration

        :param:

         - `args`: namespace with `configfiles` list
        """
        self.logger.warning('UbootKommandant.check has not been implemented')
        return

    @try_except
    def handle_help(self, args):
        """
        Sends a help message to stdout

        :param:

         - `args`: namespace with 'name' and width attributes
        """
        plugin = self.quartermaster.get_plugin(args.name)
        try:
            plugin().help(args.width)
        except TypeError as error:
            self.logger.debug(error)
            print "'{0}' is not a known plugin.\n".format(args.name)
            print "These are the known plugins:\n"
            self.quartermaster.list_plugins()
        return
#


# python standard library
import unittest

# third-party
from mock import MagicMock, patch


class TestUbootKommandant(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock('uboot_logger')
        self.subcommander = UbootKommandant()
        self.subcommander._logger = self.logger
        return

    def test_list_plugins(self):
        """
        Does it call the quarter master's list_plugins?
        """
        qm = MagicMock()
        #with patch('arachneape.plugins.quartermaster.QuarterMaster', qm):
        #    self.subcommander.list_plugins()
        #qm.list_plugins.assert_called_with()
        return
# end TestUbootKommandant
