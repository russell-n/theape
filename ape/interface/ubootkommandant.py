
# python standard library
from ConfigParser import NoSectionError
# third-party
from pycallgraph import PyCallGraph
from pycallgraph import GlobbingFilter
from pycallgraph import Config
from pycallgraph.output import GraphvizOutput

# this package
from ape.commoncode.baseclass import BaseClass
from ape.commoncode.errors import ConfigurationError
from ape.commoncode.crash_handler import try_except, log_error
from ape.commoncode.strings import RED, BOLD, RESET
from ape.plugins.quartermaster import QuarterMaster


RED_ERROR = "{red}{bold}{{error}}{reset}".format(red=RED,
                                                 bold=BOLD,
                                                 reset=RESET)


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
        self.error = (Exception, KeyboardInterrupt)
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

    def build_ape(self, args):
        """
        Tries to build the Ape plugin

        :return: ape or None
        """
        plugin = self.quartermaster.get_plugin('Ape')
        
        # The ape needs the config-filenames
        try:
            ape = plugin(configfiles=args.configfiles).product
        except ConfigurationError as error:
            self.logger.error(RED_ERROR.format(error=error))
            return
        except NoSectionError as error:
            self.logger.error(error)
            self.logger.error(RED_ERROR.format(error='[APE] section not found in {0}'.format(args.configfiles)))
            self.logger.info("Try `ape help` and `ape fetch`")
            return 
        return ape
    
    @try_except
    def run(self, args):
        """
        Builds and runs the code
        """
        ape = self.build_ape(args)
        if ape is None:
            return
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
            graphviz.output_file = 'ape_callgraph.png'
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

    def clean_up(self, error):
        """
        To be called by the try-except if an exception is caught
        """
        if type(error) is KeyboardInterrupt:
            log_error(error, self.logger, 'Oh, I am slain!')
        else:
            log_error(error, self.logger, self.error_message)
        return
        
#
