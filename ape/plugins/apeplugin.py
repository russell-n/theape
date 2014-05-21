
# python standard library
import re
import os
from collections import OrderedDict

# this package
import ape.interface.arguments.arguments as basearguments
from ape.interface.arguments.argumentbuilder import ArgumentBuilder
from ape.interface.configurationmap import ConfigurationMap
from ape.components.component import Composite
from ape.parts.storage.filestorage import FileStorage

from base_plugin import BasePlugin
from ape.commoncode.code_graphs import module_diagram, class_diagram
from ape.commoncode.errors import ApeError, DontCatchError, ConfigurationError
from ape import APESECTION, MODULES_SECTION
from quartermaster import QuarterMaster
from ape.parts.countdown.countdown import INFO
from ape.parts.countdown.countdown import CountdownTimer
import ape.commoncode.singletons as singletons


in_pweave = __name__ == '__builtin__'


DEFAULT = 'DEFAULT'
SUBFOLDER  = 'subfolder'
COMPILED_EXTENSION = '.compiled'
FILE_STORAGE_NAME = 'infrastructure'
TIMESTAMP = 'timestamp'

CONFIGURATION = '''[{0}]
# the option names are just identifiers
# they will be executed in the order given.
# Each option has to have a corresponding section below
# e.g. if there is a Sleep1 plugin listed
# Then there needs to be a [Sleep1] section below
# to configure it
<option_name_1> = <comma-separated-list of plugins>
<option_name_2> = <comma-separated-list of plugins>
...
<option_name_n> = <comma-separated-list of plugins>

# !!!! to use an option in a commented section you need to
# uncomment both the section header and the option
# if you only uncomment the option it will be assigned
# to the first un-commented section header above it, not
# necessarily the one you want

#[MODULES]
# If you are getting a plugin from a non-ape package put the module here
# it should use the import's dot-notation. e.g. :
# packagename.modulename

#[DEFAULT]
# if you add a configuration-file-glob to the default, all matching files will be added to the configuration
# even though these need to be in the ini format I like to use a different file-extension
# so they won't accidentally get picked up if you use a glob to point to the main config files
#config_glob = settings*.config

# if you want to repeat the operation defined in this config, give it repetitions
# repetitions = 1000000

# If you want to put a time limit after which to quit (this overrides repetitions)
# total_time = 1 day 3 hours

# if you want to put an end time (this will override repetitions and total time):
# end_time = November 23, 2013 8:00 am

# if you want to store files in a sub-folder
# {1} = <name>

# If you get a ParserError check:
#   - is everything flush-left?
#   - no inline comments? (this won't raise a Parser error but it will create an error later)
'''.format(APESECTION, SUBFOLDER)



output_documentation = __name__ == '__builtin__'


if in_pweave:
    this_file = os.path.join(os.getcwd(), 'apeplugin.py')
    module_diagram_file = module_diagram(module=this_file, project='apeplugin')
    print ".. image:: {0}".format(module_diagram_file)


if in_pweave:
    class_diagram_file = class_diagram(class_name="Ape",
                                       filter='OTHER',
                                       module=this_file)
    print ".. image:: {0}".format(class_diagram_file)


EXAMPLES = '''
ape run ape.ini
ape help
ape fetch
ape list'''

class Ape(BasePlugin):
    """
    The default plugin (provides the front-end for the APE)
    """
    def __init__(self, configfiles=None, *args, **kwargs):
        """
        Ape plugin Constructor

        :param:

         - `configfiles`: list of config-files to build product (Hortator Composite)
        """
        super(Ape, self).__init__(*args, **kwargs)
        self.configfiles = configfiles
        self._arguments = None
        self._quartermaster = None
        return

    @property
    def quartermaster(self):
        """
        A QuarterMaster to get Component Plugins
        """
        if self._quartermaster is None:
            self._quartermaster = QuarterMaster()
        return self._quartermaster

    @property
    def arguments(self):
        """
        The ArgumentClinic (used to set up the help-string)
        """
        if self._arguments is None:
            self._arguments = ArgumentBuilder()
        return self._arguments

    @property
    def sections(self):
        """
        An ordered dictionary for the HelpPage
        """
        if self._sections is None:
            bold = '{bold}'
            reset = '{reset}'
            
            name = __package__.split('.')[0]
            bold_name = bold + name + reset
            program = name + '[.\w]*'
            expression = re.compile(program)

            # get sample usage text
            arg_string = basearguments.__doc__.replace('Usage: ', '')
            

            # the main parser doesn't show help for the sub-commands (just --debug, --pudb, etc.)
            # so they are pulled separately
            argument_definitions = ArgumentBuilder().argument_definitions
            for definition in argument_definitions.itervalues():
                arg_string += '-' * 40 + '\n'
                arg_string +=  expression.sub(bold_name,
                                              definition().sub_usage.replace('Usage: ', ''))
            
            self._sections = OrderedDict()
            self._sections['Name'] = '{blue}' + name + reset + ' -- a plugin-based code runner'
            self._sections['Synopsis'] = arg_string
            self._sections['Description'] = bold_name + ' is the main code-runner. When it is run it looks for a configuration file or list of configuration files. Within each file it looks for an [{0}] section. Each entry in that section is interpreted to be a list of plugins to execute in top-down, left-right ordering.'.format(APESECTION)
            self._sections["Configuration"] = CONFIGURATION
            self._sections['Examples'] = 'ape run *.ini\nape help\nape fetch\nape list\nape check *ini'
            self._sections['Errors'] = '{bold}Oops, I crapped my pants:{reset} unexpected error (probably indicates implementation error)'
            self._sections['subcommands'] = "help (this help), fetch (sample configuration), run <configuration-file(s)>, list (known plugins), check (configuration)"
            self._sections['Files'] = __file__
        return self._sections
    
    @property
    def product(self):
        """
        This is the Hortator Composite product

        :precondition: self.configfiles has been set 
        :return: hortator built from self.configfiles
        """
        #create a hortator
        hortator = Composite(error=Exception,
                             identifier='Hortator',
                             error_message="Operator Crash",
                             component_category='Operator')
        # Set the TimeTracker level to info so it outputs to the screen
        hortator.time_remains.log_level = INFO
        # traverse the config-files to get Operators and configuration maps
        for config_file in self.configfiles:
            # each operation gets new singletons
            singletons.refresh()
            
            # the QuarterMaster is being created each time because I am now allowing the addition
            # of external packages, and I don't want namespace clashes
            quartermaster = QuarterMaster()

            # each APE config gets its own Operator
            operator = Composite(identifier="Operator",
                                 error=ApeError,
                                 error_message='Operation Crash',
                                 component_category='Operation')

            configuration = ConfigurationMap(config_file)
            
            defaults = configuration.defaults

            # build the countdown timer
            repetitions = configuration.get_int(section=DEFAULT,
                                                option='repetitions',
                                                optional = True,
                                                default=1)
            total_time = configuration.get_relativetime(section=DEFAULT,
                                                        option='total_time',
                                                        optional=True,
                                                        default=None)
            end_time = configuration.get_datetime(section=DEFAULT,
                                                      option='end_time',
                                                      optional=True,
                                                      default=None)
            operator.time_remains = CountdownTimer(repetitions=repetitions,
                                                   total_time=total_time,
                                                   end_time=end_time,
                                                   log_level=INFO)
            # check for external package declarations
            if MODULES_SECTION in configuration.sections:
                external_modules = [option for option in configuration.options(MODULES_SECTION)
                                    if option not in defaults]
                quartermaster.external_modules = external_modules                        
            
            # traverse the APE Section's options to get Operations
            # configuration.options(APESECTION) is a list of config-file options in the [APE] section
            # names is filtered to get rid of the DEFAULT options
            names = (name for name in configuration.options(APESECTION) if not
                     (name in defaults and
                      defaults[name] ==
                      configuration.get(APESECTION, name)))

            # the operations won't know repetitions or how long the operation has been running
            # but since end_time is an absolute time, they can check for that between operations
            countdown = None
            if end_time is not None:
                countdown = CountdownTimer(end_time=end_time)

            # the next loop is going to start building plugins, so we need to set the FileStorage now
            self.initialize_file_storage(configuration)
            
            for operation_name in names:
                # every option in the APE section gets an operation
                operation = Composite(identifier='Operation',
                                      error=DontCatchError,
                                      error_message='{0} Crash'.format(operation_name),
                                      component_category=operation_name,
                                      time_remains=countdown)

                #traverse this line to get plugins
                # get_list is a list of comma-separated strings in the operation line
                for plugin_section_name in configuration.get_list(APESECTION, operation_name):                    
                    # the quartermaster returns a class-definition, not an instance
                    # so we can pass in the configuration and build it to get the `product`

                    # in order to allow multiple configurations for the same plugin
                    # I'm detaching the section name from the plugin name
                    # this means there is a requirement that a 'plugin' field be in each
                    # plugin definition
                    plugin_name = configuration.get(plugin_section_name, 'plugin')
                    plugin_def = quartermaster.get_plugin(plugin_name)
                    try:
                        # since there are now arbitrary names for the sections
                        # either the specific section or the section name has to be passed in
                        plugin = plugin_def(configuration=configuration, section_header=plugin_section_name).product
                        if plugin is None:
                            raise ApeError("{0} is missing a `product` (returned None)".format(plugin_name))
                    except TypeError:
                        raise ConfigurationError('Could not find "{0}" plugin'.format(plugin_name))
                    operation.add(plugin)
                operator.add(operation)

            hortator.add(operator)
            # save the configuration as a copy so there will be a record
            self.save_configuration(configuration)
        return hortator

    def initialize_file_storage(self, configuration):
        """
        This has to be called before the plugins are built so the path will be set

        :param:

         - `configuration`: the Configuration (a ConfigParser like object)

        :postcondition: file-storage singleton with sub-folder from default section added as path
        """
        file_storage = singletons.get_filestorage(name=FILE_STORAGE_NAME)
        if SUBFOLDER in configuration.defaults:
            file_storage.path = configuration.defaults[SUBFOLDER]
        if TIMESTAMP in configuration.defaults:
            file_storage.timestamp = configuration.defaults[TIMESTAMP]
        return

    def save_configuration(self, configuration):
        """
        saves the configuration map to disk

        :param:

         - `configuration`: A ConfigurationMap to save to disk
        """
        file_storage = singletons.get_filestorage(name=FILE_STORAGE_NAME)
        # get the sub-folder (if given) and let the FileStorage mangle the name as needed
        # to prevent clobbering files

        filename, extension = os.path.splitext(configuration.filename)

        # the extension is changed so if the user is using a glob
        # and didn't provide a sub-folder the compiled file won't
        # get picked up on re-running the code
        filename += COMPILED_EXTENSION
        name = file_storage.safe_name(filename)
        configuration.write(name)
        return
        
    def fetch_config(self):
        """
        Prints example configuration to stdout
        """
        print CONFIGURATION
# end class Ape        
