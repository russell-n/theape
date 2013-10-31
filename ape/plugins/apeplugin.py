
# python standard library
import re
import os
from collections import OrderedDict
# this package
from ape.interface.arguments import ArgumentClinic
from ape.interface.configurationmap import ConfigurationMap
from ape.components.component import Composite

from base_plugin import BasePlugin
from ape.commoncode.code_graphs import module_diagram, class_diagram
from ape.commoncode.errors import ApeError, DontCatchError, ConfigurationError
from ape import APESECTION, MODULES_SECTION
from quartermaster import QuarterMaster


in_pweave = __name__ == '__builtin__'


CONFIGURATION = '''[{0}]
# the section names are just identifiers
# they will be executed in the order given.
<section_name_1> = <comma-separated-list of plugins>
<section_name_2> = <comma-separated-list of plugins>
...
<section_name_n> = <comma-separated-list of plugins>

[MODULES]
# If you are getting a plugin from a non-ape package put the module here
# it should use the import's dot-notation. e.g. :
# packagename.modulename

#[DEFAULT]
# if you add a configuration-file-glob to the default, all matching files will be added to the configuration
# even though these need to be in the ini format I like to use a different file-extension
# so they won't accidentally get picked up if you use a glob to point to the main config files
#config_glob = settings*.config

# if you want to store files in a sub-folder
# subfolder = <name>
'''.format(APESECTION)


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
            self._arguments = ArgumentClinic()
            self._arguments.add_arguments()
            self._arguments.add_subparsers()
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
            
            arg_string = expression.sub(name,
                                        self.arguments.parser.format_usage().replace('usage: ', ''))
            
            # the sub-parsers are listed in curly braces, breaking the text-formatting
            arg_string = arg_string.replace('{', '{{')
            arg_string = arg_string.replace('}', '}}')
            arg_string = arg_string.replace(name, bold_name)
            subs = (self.arguments.runner, self.arguments.fetcher, self.arguments.lister,
                    self.arguments.checker, self.arguments.helper)
            for sub in subs:
                arg_string +=  expression.sub(bold_name,
                                              sub.format_usage().replace('usage: ', ''))
            
            self._sections = OrderedDict()
            self._sections['Name'] = '{blue}' + name + reset + ' -- a plugin-based code runner'
            self._sections['Synopsis'] = arg_string
            self._sections['Description'] = bold_name + ' is a code-runner. When it is run it looks for a configuration file or list of configuration files. Within each file it looks for an [{0}] section. Each entry in that section is interpreted to be a list of plugins to execute in top-down, left-right ordering.'.format(APESECTION)
            self._sections["Configuration"] = CONFIGURATION
            self._sections['Examples'] = 'ape run *.ini\nape help\nape fetch\nape list\nape check *ini'
            self._sections['Errors'] = '{bold}Oops, I crapped my pants:{reset} unexpected error (probably indicates implementation error)'
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
                             component_category='Operator',
                             is_root=True)

        # traverse the config-files to get Operators and configuration maps
        for config in self.configfiles:
            # this is being created each time because I am now allowing the addition
            # of external packages, and I don't want namespace clashes
            quartermaster = QuarterMaster()
            operator = Composite(identifier="Operator",
                                 error=ApeError,
                                 error_message='Operation Crash',
                                 component_category='Operation')
            configuration = ConfigurationMap(config)
            defaults = configuration.defaults

            # check for external package declarations
            if MODULES_SECTION in configuration.sections:
                external_modules = [option for option in configuration.options(MODULES_SECTION)
                                    if option not in defaults]
                quartermaster.external_modules = external_modules                        
            
            # traverse the APE Section's options to get Operations
            #options(APESECTION) is a list of config-file options
            names = (name for name in configuration.options(APESECTION) if not
                     (name in defaults and
                      defaults[name] ==
                      configuration.get(APESECTION, name)))
            
            for operation_name in names:
                operation = Composite(identifier='Operation',
                                      error=DontCatchError,
                                      error_message='{0} Crash'.format(operation_name),
                                      component_category=operation_name)
                                
                #traverse this line to get plugins
                # get_list is a list of comma-separated strings in the operation line
                for plugin_name in configuration.get_list(APESECTION, operation_name):                    
                    # the quartermaster returns a class-definition, not an instance
                    # so we can pass in the configuration and build it to get the `product`
                    plugin_def = quartermaster.get_plugin(plugin_name)
                    try:
                        plugin = plugin_def(configuration).product
                        if plugin is None:
                            raise ApeError("{0} is missing a `product` (returned None)".format(plugin_name))
                    except TypeError:
                        raise ConfigurationError('Could not find "{0}" plugin'.format(plugin_name))
                    operation.add(plugin)
                operator.add(operation)
            # ** Add saving the configuration here
            hortator.add(operator)
        return hortator

    def fetch_config(self):
        """
        Prints example configuration to stdout
        """
        print CONFIGURATION
# end class Ape        


if output_documentation:
    arguments = ArgumentClinic()
    arguments.add_arguments()
    arguments.add_subparsers()
    parser = arguments.parser
    print parser.format_usage()


if output_documentation:
    parser.prog = 'ape'
    print parser.format_help()


if output_documentation:
    subs = (arguments.runner, arguments.fetcher,
            arguments.lister, arguments.checker, arguments.helper)

    program = 'ape[.\w]*'
    expression = re.compile(program)
    for sub in subs:
        print expression.sub('ape', sub.format_usage().replace('usage: ', ''))
