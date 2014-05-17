
"""`run` sub-command

Usage: ape run -h
       ape run [<configuration>...]

Positional Arguments:

    <configuration>   0 or more configuration-file names [default: ape.ini]

Options;

    -h, --help  This help message.

"""


# the APE
from ape.interface.arguments.arguments import BaseArguments


class RunArgumentsConstants(object):
    """
    Constants for the Run Arguments
    """
    __slots__ = ()
    configfiles = '<configuration>'
    
    # defaults
    default_configfiles = ['ape.ini']
# RunArgumentsConstants    


class RunArguments(BaseArguments):
    """
    Arguments for the `run` sub-command
    """
    def __init__(self, *args, **kwargs):
        super(RunArguments, self).__init__(*args, **kwargs)
        self._configfiles = None
        self.sub_usage = __doc__
        self._function = None
        return

    @property
    def function(self):
        """
        sub-command function 
        """
        if self._function is None:
            self._function = self.subcommands.run
        return self._function

    @property
    def configfiles(self):
        """
        List of config-file names
        """
        if self._configfiles is None:
            self._configfiles = self.sub_arguments[RunArgumentsConstants.configfiles]
            if not self._configfiles:
                self._configfiles = RunArgumentsConstants.default_configfiles
        return self._configfiles

    def reset(self):
        """
        Resets the attributes to None
        """
        super(RunArguments, self).reset()
        self._configfiles = None
        return
# end RunArguments        
