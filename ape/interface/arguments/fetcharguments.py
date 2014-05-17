
"""fetch subcommand
    
usage: ape fetch -h
       ape fetch [<name>...]  [--module <module> ...] 

positional arguments:
    <name>                         List of plugin-names (default=['Ape'])

optional arguments:
    -h, --help                     Show this help message and exit
    -m, --module <module> ...      Non-ape modules
"""


# the APE
from ape.interface.arguments.arguments import BaseArguments


class FetchArgumentsConstants(object):
    """
    Constants for the `fetch` sub-command arguments
    """    
    __slots__ = ()
    # arguments and options
    names = "<name>"
    modules = '--module'
    
    # defaults
    default_names = ['Ape']


class FetchArguments(BaseArguments):
    """
    Arguments for the `fetch` sub-command
    """
    def __init__(self, *args, **kwargs):
        super(FetchArguments, self).__init__(*args, **kwargs)
        self.sub_usage = __doc__
        self._names = None
        self._modules = None
        self._function = None
        return

    @property
    def function(self):
        """
        fetch sub-command
        """
        if self._function is None:
            self._function = self.subcommands.fetch
        return

    @property
    def names(self):
        """
        List of plugin names to use
        """
        if self._names is None:
            self._names = self.sub_arguments[FetchArgumentsConstants.names]
            if not self._names:
                self._names = FetchArgumentsConstants.default_names
        return self._names

    @property
    def modules(self):
        """
        List of modules holding plugins
        """
        if self._modules is None:
            self._modules = self.sub_arguments[FetchArgumentsConstants.modules]
        return self._modules
    
    def reset(self):
        """
        Resets the attributes to None
        """
        super(FetchArguments, self).reset()
        self._modules = None
        self._names = None
        return
# end FetchArguments    
