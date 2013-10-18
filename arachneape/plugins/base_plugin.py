
# python standard library
from abc import ABCMeta, abstractmethod, abstractproperty
import os

# this package 
from arachneape.commoncode.baseclass import BaseClass
from arachneape.components.helppage.helppage import HelpPage
from arachneape.commoncode.code_graphs import module_diagram, class_diagram


in_pweave = __name__ == '__builtin__'


if in_pweave:
    this_file = os.path.join(os.getcwd(), 'base_plugin.py')
    module_diagram_file = module_diagram(module=this_file, project='baseplugin')
    print ".. image:: {0}".format(module_diagram_file)


if in_pweave:
    class_diagram_file = class_diagram(class_name="BasePlugin",
                                       filter='OTHER',
                                       module=this_file)
    print ".. image:: {0}".format(class_diagram_file)


class BasePlugin(BaseClass):
    """
    An abstract base-class for plugins

    :param:

     - `configuration`: configuration-map for plugin configuration
    """
    def __init__(self, configuration=None):
        super(BasePlugin, self).__init__()
        self._logger = None
        self._help = None
        self._config = None
        self._product = None
        self._help_page = None        
        self._sections = None
        return

    @abstractproperty
    def sections(self):
        """
        A (ordered) dictionary for the help page
        """
        return self._sections

    @property
    def help_page(self):
        """
        A HelpPage to use if self.sections has been defined
        """
        if self._help_page is None and self.sections is not None:
            self._help_page = HelpPage(sections=self.sections)
        return self._help_page                        

    def help(self, width=80):
        """
        Prints a help-string for the plugin

        :param:

         - `width`: number of characters wide to print help
        """
        if self.sections is None:
            print "'{0}' offers you no help. Such is life.".format(self.__class__.__name__)
        else:
            self.help_page.wrap = width
            self.help_page()
        return

    @abstractproperty
    def product(self):
        """
        The plugin (BaseProduct implementation)
        """
        return

    @abstractmethod
    def fetch_config(self):
        """
        Get sample config-file snippet required by this plugin
        """
        return   
# end class BasePlugin                
