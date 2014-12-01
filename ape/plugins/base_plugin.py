
# python standard library
from abc import ABCMeta, abstractmethod, abstractproperty
import os
from types import StringType

# third party
from configobj import ConfigObj, flatten_errors, get_extra_values
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


class BaseConfigurationConstants(object):
    """
    Holder of BaseConfiguration constants
    """
    __slots__ = ()
    plugin_option ='plugin'
    error_name = 'ConfigurationError'
    bad_option_message = "Option '{option}' in section '{section}' failed validation (error='{error}', should be {option_type})"
    missing_option_message = "Option '{option}' in section '{section}' of type {option_type} required but missing"
    missing_section_message = "Section '{section}' to configure '{plugin}' not found in configuration"
    extra_message = "Extra {item_type} in section '{section}. '{name}'"


class BaseConfiguration(BaseClass):
    """
    Abstract base class for configurations
    """
    __metaclass__ = ABCMeta
    def __init__(self, source, section_name, configspec_source=None):
        """
        BaseConfiguration constructor

        :param:

         - `source`: ConfigObj section
         - `section_name`: section-name in the configuration
         - `configspec_source`: list or file with configspec
        """
        super(BaseConfiguration, self).__init__()
        self.section_name = section_name
        self.source = source
        self._configspec_source = configspec_source
        
        self._product = None
        self._validator = None
        self._configspec = None
        self._configuration = None
        self._plugin_name = None
        self._section = None
        self._validation_outcome = None
        return

    @property
    def validation_outcome(self):
        """
        Outcome of validating the configuration
        """
        if self._validation_outcome is None:
            self._validation_outcome = self.configuration.validate(self.validator,
                                                                   preserve_errors=True)
        return self._validation_outcome

    @property
    def section(self):
        """
        Section extracted using self.section_name (if section_name not in config, sets to self.configuration)
        """
        if self._section is None:
            try:
                self._section = self.configuration[self.section_name]
            except KeyError as error:
                self.logger.debug(error)
                self._section = self.configuration
        return self._section

    @property
    def plugin_name(self):
        """
        Gets the plugin name from the section (or empty string if missing)
        """
        if self._plugin_name is None:
            try:
                self._plugin_name = self.section[BaseConfigurationConstants.plugin_option]
            except KeyError as error:
                self.logger.warning("'plugin' option missing in section '{0}'".format(self.section_name))
                self._plugin_name = ''
        return self._plugin_name

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
            # chicken-and-egg problem using configspec_source property
            # so I'm changing it here
            configspec_source = self.configspec_source
            if type(self.configspec_source) is StringType:
                # if source has string format option {section_name}
                # don't change the original because configuration property needs it
                configspec_source = self.configspec_source.format(section_name=self.section_name)
                configspec_source = configspec_source.splitlines()
            self._configspec = ConfigObj(configspec_source,
                                         list_values=False,
                                         _inspec=True)
        return self._configspec


    @property
    def configuration(self):
        """
        validates and sets the configuration using the source configuration

        :precondition: self.configspec has full configspec including section name
        :postcondition: self.source is validated configuration
        :postcondition: self.outcome is the outcome of the validation
        """
        if self._configuration is None:
            configuration = ConfigObj(self.source,
                                        configspec=self.configspec,
                                        file_error=True)
            self._validation_outcome = configuration.validate(self.validator,
                                                            preserve_errors=True)

            #if self.source[self.section_name]['updates_section'] is not None:
            #    other_section = self.source[self.section_name]['updates_section']
            #    configspec_source = self.configspec_source.format(section_name=other_section)
            #    configspec_source = configspec_source.splitlines()
            #    configspec = ConfigObj(configspec_source,
            #                           list_values=False,
            #                           _inspec=True)
            #    original_section = ConfigObj(self.source,
            #                                 configspec=configspec,
            #                                 file_error=True)
            #    original_section.validate(self.validator,
            #                              preserve_errors=True)
            #    original_section.merge(configuration)
            #    configuration = original_section
            #    self._validation_outcome = configuration.validate(self.validator,
            #                                                      preserve_errors=True)
            self._configuration = configuration
            
        return self._configuration

    @abstractproperty
    def configspec_source(self):
        """
        Source for configuration specification (probably list of lines)
        """
        return

    @abstractproperty
    def product(self):
        """
        The object built from the configuration
        """
        return

    def process_errors(self):
        """
        logs the errors in outcome

        :param:

         - `outcome`: output of `validate` call
        """
        constants = BaseConfigurationConstants
        for sections, option, error in flatten_errors(self.configuration,
                                                      self.validation_outcome):
            section = ",".join(sections)
            if not section:
                section = self.section_name

            if option is not None: # something is wrong with the option
                # if there are sub-sections then the configspec has to be traversed to get the option-type
                spec = self.configspec
                for section in sections:
                    spec = spec[section]
                option_type = spec[option]
                
                if error: # validation of option failed                    
                    self.log_error(error=constants.error_name,
                                   message=constants.bad_option_message.format(option=option,
                                                                               section=section,
                                                                               error=error,
                                                                               option_type=option_type))
                else: # missing option
                    self.log_error(error=constants.error_name,
                                   message=constants.missing_option_message.format(option=option,
                                                                                   section=section,
                                                                                   option_type=option_type))
            else: # section missing
                print ",".join(sections)
                self.log_error(error=constants.error_name,
                               message=constants.missing_section_message.format(section=section,
                                                                                plugin=self.plugin_name))
        return

    def check_extra_values(self, warn_user=True):
        """
        checks the configuration for values not in the configspec

        :return: True if extra values, false otherwise
        """
        if warn_user:
            logger = self.logger.warning
        else:
            # in case the plugin doesn't care
            logger = self.logger.debug
            
        extra_values = get_extra_values(self.configuration)

        for sections, name in extra_values:
            # sections is a tuple of all the sections and subsections
            # leading to the option so we have to get to the bottom
            bottom_section = self.configuration
            for section in sections:
                bottom_section = bottom_section[section]

            # value is the extra item (either a value or section)
            value = bottom_section[name]
            
            item_type = 'option'
            if isinstance(value, dict):
                item_type = 'section'
            
            section = ','.join(sections) or "top level"
            message = BaseConfigurationConstants.extra_message.format(section=section,
                                                                    item_type=item_type,
                                                                    name=name)
            if item_type == 'option':
                message += "='{0}'".format(value)
            logger(message)
                
        return len(extra_values)
# end BaseConfiguration        
