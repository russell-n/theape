
# python standard library
import re
import os
from collections import OrderedDict
# this package
from arachneape.interface.arguments import ArgumentClinic
from arachneape.interface.configurationmap import ConfigurationMap
from arachneape.components.component import Composite

from base_plugin import BasePlugin
from arachneape.commoncode.code_graphs import module_diagram, class_diagram
from arachneape.commoncode.errors import ApeError, DontCatchError
from arachneape.commoncode.constants import APESECTION
from quartermaster import QuarterMaster


in_pweave = __name__ == '__builtin__'


CONFIGURATION = '''[ARACHNEAPE]
# the section names are just identifiers
# they will be executed in alphabetical order
<section_name_1> = <comma-separated-list of plugins>
<section_name_2> = <comma-separated-list of plugins>
...
<section_name_n> = <comma-separated-list of plugins>                        
'''


output_documentation = __name__ == '__builtin__'


if in_pweave:
    this_file = os.path.join(os.getcwd(), 'arachneapeplugin.py')
    module_diagram_file = module_diagram(module=this_file, project='arachneapeplugin')
    print ".. image:: {0}".format(module_diagram_file)


if in_pweave:
    class_diagram_file = class_diagram(class_name="ArachneApe",
                                       filter='OTHER',
                                       module=this_file)
    print ".. image:: {0}".format(class_diagram_file)


EXAMPLES = '''
arachneape run ape.ini
arachneape help
arachneape fetch
arachneape list'''

class ArachneApe(BasePlugin):
    """
    The default plugin
    """
    def __init__(self, configfiles=None, *args, **kwargs):
        """
        ArachneApe plugin

        :param:

         - `configfiles`: list of config-files to build product (Composite)
        """
        super(ArachneApe, self).__init__(*args, **kwargs)
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
        The ArgumentClinic
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
            self._sections['Description'] = bold_name + ' is a code-runner. When it is run it looks for a configuration file or list of configuration files. Within each file it looks for an [ARACHNEAPE] section. Each entry in that section is interpreted to be a list of plugins to execute in top-down, left-right ordering.'
            self._sections["Configuration"] = CONFIGURATION
            self._sections['Examples'] = 'arachneape run *.ini\narachneape help\narachneape fetch\narachneape list\narachneape check *ini'
            self._sections['Errors'] = 'Nothing yet'
            self._sections['Files'] = __file__
        return self._sections
    
    @property
    def product(self):
        """
        this is a product

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
            operator = Composite(identifier="Operator",
                                 error=ApeError,
                                 error_message='Operation Crash',
                                 component_category='Operation')
            configuration = ConfigurationMap(config)
            defaults = configuration.defaults
            
            # traverse the APE Section's options to get Operations
            #options(apesection) is a list of config file lines
            for operation_name in configuration.options(APESECTION):
                # The DEFAULT section will polute the APESECTION namespace -check for it
                if (operation_name in defaults and
                    defaults[operation_name] ==
                    configuration.get(APESECTION, operation_name)):
                        # this won't work if they are coincidentally the same.
                        continue
                # get_list is a list of comma-separated strings in the operation line
                operation = Composite(identifier='Operation',
                                      error=DontCatchError,
                                      error_message='{0} Crash'.format(operation_name),
                                      component_category=operation_name)

                #traverse this line to get plugins
                for plugin_name in configuration.get_list(APESECTION, operation_name):                    
                    # the quartermaster returns a class-definition, not an instance                    
                    plugin_def = self.quartermaster.get_plugin(plugin_name)
                    try:
                        plugin = plugin_def(configuration).product
                    except TypeError:
                        self.logger.error('Could not find "{0}" plugin'.format(plugin_name))
                        raise
                    operation.add(plugin)
                operator.add(operation)
            # ** Add saving the configuration here
            hortator.add(operator)
        return hortator

    def fetch_config(self):
        """
        Prints example configuration
        """
        print CONFIGURATION
# end class ArachnePlugin        


if output_documentation:
    arguments = ArgumentClinic()
    arguments.add_arguments()
    arguments.add_subparsers()
    parser = arguments.parser
    print parser.format_usage()


if output_documentation:
    parser.prog = 'arachneape'
    print parser.format_help()


if output_documentation:
    subs = (arguments.runner, arguments.fetcher,
            arguments.lister, arguments.checker, arguments.helper)

    program = 'arachneape[.\w]*'
    expression = re.compile(program)
    for sub in subs:
        print expression.sub('arachneape', sub.format_usage().replace('usage: ', ''))
