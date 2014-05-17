
"""`help` sub-command

usage: ape help -h
       ape help [-w WIDTH] [--module <module>...] [<name>]

positional arguments:
    <name>                A specific plugin to inquire about [default: Ape].

optional arguments:
    -h, --help            show this help message and exit
    -w , --width <width>  Number of characters to wide to format the page. [default: 80]
    -m, --module <module>     non-ape module with plugins
    
"""


# the ape
from ape.interface.arguments.arguments import BaseArguments


class HelpArgumentsConstants(object):
    """
    Constants for the `help` sub-command arguments 
    """
    __slots__ = ()
    width = '--width'
    modules = '--module'
    name = "<name>"

    default_name = 'Ape'


class HelpArguments(BaseArguments):
    """
    Arguments for the `help` sub-command
    """
    def __init__(self, *args, **kwargs):
        super(HelpArguments, self).__init__(*args, **kwargs)
        self._width = None
        self._modules = None
        self._name = None
        self.sub_usage = __doc__
        self._function = None
        return

    @property
    def function(self):
        """
        `help` sub-command
        """
        if self._function is None:
            self._function = self.subcommands.handle_help
        return self._function
            
    @property
    def width(self):
        """
        Option to set the width of the text
        """
        if self._width is None:
            self._width = int(self.sub_arguments[HelpArgumentsConstants.width])
        return self._width

    @property
    def modules(self):
        """
        Optional list of modules with plugins
        """
        if self._modules is None:
            self._modules = self.sub_arguments[HelpArgumentsConstants.modules]
        return self._modules

    @property
    def name(self):
        """
        Option for the name of the plugin
        """
        if self._name is None:
            self._name = self.sub_arguments[HelpArgumentsConstants.name]
            if not self._name:
                self._name = HelpArgumentsConstants.default_name
        return self._name
    
    def reset(self):
        """
        Resets the properties to None
        """
        super(HelpArguments, self).reset()
        self._width = None
        self._modules = None
        self._name = None
        return
# end HelpArguments    
