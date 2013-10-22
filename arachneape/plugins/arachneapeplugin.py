
# python standard library
import re
import os
from collections import OrderedDict
# this package
from arachneape.interface.arguments import ArgumentClinic
from arachneape.components.component import Composite
from arachneape.parts.dummy.dummy import DummyClass
from base_plugin import BasePlugin
from arachneape.commoncode.code_graphs import module_diagram, class_diagram
from arachneape.commoncode.errors import ApeError, DontCatchError


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
    def __init__(self, *args, **kwargs):
        super(ArachneApe, self).__init__(*args, **kwargs)
        self._arguments = None
        return

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
        """
        class Leaf(DummyClass):
            def __init__(self, *args, **kwargs):
                super(Leaf, self).__init__(*args, **kwargs)

        class BadLeaf(Leaf):
            def __init__(self, *args, **kwargs):
                super(BadLeaf, self).__init__(*args, **kwargs)
                
            def __call__(self):
                raise ApeError('this is a component error')

        # some component leaves
        leaf_1 = Leaf(name='leaf_1')
        leaf_2 = Leaf(name='leaf_2')            
        leaf_3 = BadLeaf(name='leaf_3')

        #  operator
        operator = Composite(error=ApeError,
                             error_message='Operation Crash',
                             component_category='Operation')
        operator_2 = Composite(error=ApeError,
                               error_message='Operation Crash',
                               component_category='Operation')


        # first operation
        operation_1 = Composite(error=DontCatchError,
                                error_message='Component Crash',
                                component_category='Component')
        
        operation_2 = Composite(error=DontCatchError,
                                error_message='Component Crash',
                                component_category='Component')

        operation_3 = Composite(error=DontCatchError,
                                error_message='Component Crash',
                                component_category='Component')

        operation_1.add(leaf_1)
        operation_1.add(leaf_3)
        operation_2.add(leaf_2)
        
        operator.add(operation_1)
        operator.add(operation_2)

        operation_3.add(leaf_3)
        operation_3.add(leaf_1)
        operator_2.add(operation_3)
        # second 
        exhort = Composite(error=Exception,
                           error_message="Operator Crash",
                           component_category='Operator',
                           is_root=True)
        exhort.add(operator)
        exhort.add(operator_2)
        return exhort

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
