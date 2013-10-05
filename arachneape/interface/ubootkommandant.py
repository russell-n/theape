
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
            return method(*args, **kwargs)
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
    def list_plugins(self):
        """
        calls the QuarterMaster and lists plugins
        """
        self.quartermaster.list_plugins()
        return
# end class UbootKommandant    


# python standard library
import unittest

# third-party
from mock import MagicMock, patch


class TestUbootKommandant(unittest.TestCase):
    def setUp(self):
        self.subcommander = UbootKommandant()
        return

    def test_list_plugins(self):
        """
        Does it call the quarter master's list_plugins?
        """
        qm = MagicMock()
        with patch('arachneape.plugins.quartermaster.QuarterMaster', qm):
            self.subcommander.list_plugins()
        #qm.list_plugins.assert_called_with()
        return
# end TestUbootKommandant
