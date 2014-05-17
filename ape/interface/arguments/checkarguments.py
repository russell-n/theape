
"""`check` sub-command

usage: ape check -h
       ape check  [<config-file-name> ...] [--module <module> ...]

Positional Arguments:

    <config-file-name> ...    List of config files (e.g. *.ini - default='['ape.ini']')

optional arguments:

    -h, --help                  Show this help message and exit
    -m, --module <module>       Non-ape module with plugins

"""


# third-party
import docopt

# this package
from ape.interface.arguments.arguments import BaseArguments, ArgumentsConstants


class CheckArgumentsConstants(object):
    """
    A holder of constants for the Check Sub-Command Arguments
    """
    __slots__ = ()
    # options and arguments
    configfilenames = "<config-file-name>"
    modules = "--module"

    #defaults
    default_configfilenames = ['ape.ini']


class CheckArguments(BaseArguments):
    """
    Arguments for the check sub-command
    """
    def __init__(self, *args, **kwargs):
        super(CheckArguments, self).__init__(*args, **kwargs)
        self._configfiles = None
        self._modules = None
        self.sub_usage = __doc__
        self._function = None
        return

    @property
    def function(self):
        """
        The `check` sub-command 
        """
        if self._function is None:
            self._function = self.subcommands.check
        return self._function

    @property
    def configfiles(self):
        """
        List of configuration file names.
        """
        if self._configfiles is None:
            self._configfiles = self.sub_arguments[CheckArgumentsConstants.configfilenames]
            if not self._configfiles:
                self._configfiles = CheckArgumentsConstants.default_configfilenames
        return self._configfiles

    @property
    def modules(self):
        """
        List of optional modules
        """
        if self._modules is None:
            self._modules = self.sub_arguments[CheckArgumentsConstants.modules]
        return self._modules
    
    def reset(self):
        """
        Resets the properties to None
        """
        super(CheckArguments, self).reset()
        self._sub_arguments = None
        self._configfiles = None
        self._modules = None
        return
#end CheckArguments    
