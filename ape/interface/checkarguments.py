
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
from ape.interface.arguments import BaseArguments, ArgumentsConstants


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
        self._configfilenames = None
        self._sub_arguments = None
        self._modules = None
        return

    @property
    def sub_arguments(self):
        """
        the sub-argument dictionary
        """
        if self._sub_arguments is None:
            self._sub_arguments = docopt.docopt(doc=__doc__,
                                                argv=[self.arguments[ArgumentsConstants.command]] +
                                                self.arguments[ArgumentsConstants.argument])
        return self._sub_arguments            

    @property
    def configfilenames(self):
        """
        List of configuration file names.
        """
        if self._configfilenames is None:
            self._configfilenames = self.sub_arguments[CheckArgumentsConstants.configfilenames]
            if not self._configfilenames:
                self._configfilenames = CheckArgumentsConstants.default_configfilenames
        return self._configfilenames

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
        self._configfilenames = None
        self._modules = None
        return
#end CheckArguments    
