
# python standard library
import os
import importlib

# this package
from arachneape.commoncode.baseclass import BaseClass
from base_plugin import BasePlugin


class QuarterMaster(BaseClass):
    """
    A plugin manager
    """
    def list_plugins(self):
        for filename in os.listdir(os.getcwd()):
            if filename.endswith('.py') and not filename=='quartermaster.py':
                base, extension = os.path.splitext(filename)
                candidate = importlib.import_module(base)
                # isclass is because not all objects have __base__
                members = inspect.getmembers(candidate, lambda o: inspect.isclass(o) and o.__base__ is PluginBase)
                for member in members:
                    name, definition = member
                    print name        

        return


# python standard library
import unittest

# third party
from mock import patch


class TestQuarterMaster(unittest.TestCase):
    def setUp(self):
        self.quartermaster = QuarterMaster()

        # setup the patches
        self.listdir_patch = patch('os.listdir')
        self.mock_listdir = self.listdir_patch.start()
        self.plugin_names = 'a.py b.py c.py'.split()
        self.not_plugins = 'index.pnw index.rst index.py'.split()
        self.mock_listdir.return_value = self.plugin_names + self.not_plugins
        return

    def tearDown(self):
        self.mock_listdir.stop()
        return
    
