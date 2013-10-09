
# this package
from arachneape.commoncode.baseclass import BaseClass
from arachneape.plugins.quartermaster import QuarterMaster


def try_except(method):
    """
    A decorator method to catch Exceptions

    :param:

     - `func`: A function to call
    """
    def wrapped(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception as error:
            import traceback
            self.logger.error(error)
            self.logger.debug(traceback.format_exc())
    return wrapped


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
        self.logger.warning('UbootKommandant.run has not been implemented')
        return

    @try_except
    def fetch(self, args):
        """
        'fetch' a sample plugin config-file

        :param:

         - `args`: namespace with 'names' list attribute
        """
        self.quartermaster.fetch(args.names)
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

         - `args`: namespace with a 'name' attribute
        """
        plugin = self.quartermaster.get_plugin(args.name)
        print plugin().help
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
