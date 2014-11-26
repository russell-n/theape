
# python standard library
from abc import ABCMeta, abstractmethod, abstractproperty
import os

# third party
from configobj import ConfigObj
from validate import Validator

# this package 
from ape.infrastructure.baseclass import BaseClass
from ape.parts.helppage.helppage import HelpPage
from ape.infrastructure.code_graphs import module_diagram, class_diagram


in_pweave = __name__ == '__builtin__'


class BasePlugin(BaseClass):
    """
    An abstract base-class for plugins

    :param:

     - `configuration`: configuration-map for plugin configuration
    """
    __metaclass__ = ABCMeta
    def __init__(self, configuration=None, section_header=None):
        """
        BasePlugin constructor

        :param:

         - `configuration`: a ConfigObj for the product
         - `section_header`: header in the configuration for this plugin's info
        """
        super(BasePlugin, self).__init__()
        self._logger = None
        self._help = None
        self._config = None
        self._product = None
        self._help_page = None        
        self._sections = None
        self.configuration = configuration
        self.section_header = section_header
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
        Abstract Property: The plugin (Component implementation)
        """
        return

    @abstractmethod
    def fetch_config(self):
        """
        Abstract Method: Get sample config-file snippet required by this plugin
        """
        return   
# end class BasePlugin                


class BaseConfiguration(object):
    """
    Abstract base class for configurations
    """
    __metaclass__ = ABCMeta
    def __init__(self, configuration, section_name, configspec_source):
        """
        BaseConfiguration constructor

        :param:

         - `configuration`: ConfigObj section
         - `section_name`: section-name in the configuration
         - `configspec_source`: list or file with configspec
        """
        self.section_name = section_name
        self._product = None
        self._validator = None

        # these require previous arguments
        self.configspec_source = configspec_source
        self._configspec = None
        self._configuration = None
        self.configuration = configuration
        return

    @property
    def validator(self):
        """
        validator for the configuration
        """
        if self._validator is None:
            self._validator = Validator()
        return self._validator

    @property
    def configspec(self):
        """
        A configspec that  matches the Configuration
        """
        if self._configspec is None:
            self._configspec = ConfigObj(self.configspec_source,
                                         list_values=False,
                                         _inspec=True)
        return self._configspec


    @property
    def configuration(self):
        return self._configuration

    @configuration.setter
    def configuration(self, new_configuration):
        """
        validates and sets the configuration using the new_configuration

        :precondition: self.section_name is section in the new_configuration
        :postcondition: self._configuration is validated configuration
        """
        self._configuration = ConfigObj(new_configuration[self.section_name],
                                        configspec=self.configspec,
                                        file_error=True)
        self._configuration.validate(self.validator)
        return

    @abstractproperty
    def product(self):
        """
        The object built from the configuration
        """
        return
