
# python standard library
import unittest

# third-party
from mock import MagicMock, patch

# this package
from ape.interface.ubootkommandant import UbootKommandant


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
        #with patch('ape.plugins.quartermaster.QuarterMaster', qm):
        #    self.subcommander.list_plugins()
        #qm.list_plugins.assert_called_with()
        return
# end TestUbootKommandant
