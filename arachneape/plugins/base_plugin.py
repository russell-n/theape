
# python standard library
from abc import ABCMeta, abstractmethod, abstractproperty

# this package 
from arachneape.commoncode.baseclass import BaseClass
from arachneape.components.helppage.helppage import HelpPage


class BasePlugin(BaseClass):
    """
    An abstract base-class for plugins
    """
    __metaclass__ = ABCMeta
    def __init__(self, configuration=None):
        super(BasePlugin, self).__init__()
        self._logger = None
        self._help = None
        self._config = None
        self._product = None
        self._help_page = None        
        self._sections = None
        return

    @property
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

    def fetch_config(self):
        """
        Get sample config-file snippet required by this plugin
        """
        print "'{0}' has no configuration sample.".format(self.__class__.__name__)
        return   
# end class BasePlugin                
