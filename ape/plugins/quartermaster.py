
# python standard library
import os
import importlib
import inspect

# this package
from ape.commoncode.baseclass import BaseClass
from base_plugin import BasePlugin
from ape.commoncode.code_graphs import module_diagram, class_diagram


document_this = __name__ == '__builtin__'


if document_this:
    this_file = os.path.join(os.getcwd(), 'quartermaster.py')
    module_diagram_file = module_diagram(module=this_file, project='quartermaster')
    print ".. image:: {0}".format(module_diagram_file)


if document_this:
    class_diagram_file = class_diagram(class_name="QuarterMaster",
                                       filter='OTHER',
                                       module=this_file)
    print ".. image:: {0}".format(class_diagram_file)


class QuarterMaster(BaseClass):
    """
    A plugin manager
    """
    def __init__(self, external_modules=None):
        """
        The Plugin Manager

        :param:

         - `external_modules`: iterable collection of module-names
        """
        super(QuarterMaster, self).__init__()
        self._plugins = None
        self.external_modules = None
        return

    @property
    def filenames(self):
        """
        A generator of python file-names from this directory
        """
        exclude = "__init__.py index.py constants.py quartermaster.py".split()
        dirname = os.path.dirname(__file__)
        return (name for name in os.listdir(dirname) if name.endswith('.py') and name not in exclude)

    @property
    def modules(self):
        """
        A generator of candidate modules from this directory
        """        
        basenames_extensions = (os.path.splitext(name) for name in self.filenames)
        return (importlib.import_module('.'.join((__package__, base)))
                for base, extension in basenames_extensions)

    @property
    def plugins(self):
        """
        A dictionary of plugins (this is persistent, unlike the generators, in case it gets re-used)
        """
        if self._plugins is None:
            from ape.plugins.base_plugin import BasePlugin
            self._plugins = {}
            
            def is_plugin(o):
                return (inspect.isclass(o)
                        and o.__base__ is BasePlugin)
            
            for module in self.modules:
                members = inspect.getmembers(module,
                                             predicate=is_plugin)
                for member in members:
                    name, definition = member
                    self._plugins[name] = definition
            # check if external modules were given
            if self.external_modules is not None:
                for candidate in self.external_modules:
                    module = importlib.import_module(candidate)
                    members = inspect.getmembers(module,
                                             predicate=is_plugin)
                    for member in members:
                        name, definition = member
                        self._plugins[name] = definition                    
        return self._plugins        
    
    def list_plugins(self):
        """
        Prints the names of the plugins to standard out
        """
        for name in sorted(self.plugins.keys()):
            print name
        return

    def get_plugin(self, name):
        """
        Retrieves a plugin object.

        :param:

         - `name`: The name of a plugin class
         - `configuration`: A configuration map instance

        :return: An un-built plugin object definition
        """
        self.logger.debug("Retrieving {0}".format(name))
        try:
            return self.plugins[name]
        except KeyError as error:
            self.logger.error(error)
        return
# end class QuarterMaster    


if document_this:
    import ape.plugins.base_plugin as base_plugin
    print base_plugin.__file__


if document_this:
    path = os.path.dirname(base_plugin.__file__)
    for name in sorted(name for name in os.listdir(path) if name.endswith('.py')):
        print name


if document_this:
    print base_plugin.__package__


if document_this:
    # remember we need the package
    package = base_plugin.__package__
    exclude = "__init__.py index.py constants.py quartermaster.py".split()
    names = sorted(name for name in os.listdir(path)
                   if name.endswith('.py') and not name in exclude)
    basenames_extensions = (os.path.splitext(name) for name in names)
    modules = (importlib.import_module('.'.join((package, base))) for base, extension in basenames_extensions)


if document_this:
    isclass = inspect.isclass
    def is_plugin(o):
        return isclass(o) and o.__base__ is BasePlugin
            
    for module in modules:
        members = inspect.getmembers(module,
                                     predicate=is_plugin)
        for member in members:
            # each member is a tuple
            name, definition = member
            print name
            plugin = definition(None)


if document_this:
    import ape.plugins.base_plugin
    names = sorted(name for name in os.listdir(path)
                   if name.endswith('.py') and not name in exclude)
    basenames_extensions = (os.path.splitext(name) for name in names)
    modules = (importlib.import_module('.'.join((package, base))) for base, extension in basenames_extensions)

    def is_plugin(o):
        return isclass(o) and o.__base__ is ape.plugins.base_plugin.BasePlugin
    
    for module in modules:
        members = inspect.getmembers(module,
                                     predicate=is_plugin)
        for member in members:
            # each member is a tuple
            name, definition = member
            print name
            plugin = definition(None)


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
    
