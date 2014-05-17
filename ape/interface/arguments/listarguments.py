
"""list subcommand

usage: ape list -h
       ape list [<module> ...]

Positional Arguments:
  <module> ...  Space-separated list of importable module with plugins

optional arguments:

  -h, --help                 Show this help message and exit

"""


# the ape
from ape.interface.arguments.arguments import BaseArguments


class ListArgumentsConstants(object):
    """
    Constants for the list sub-command arguments
    """
    __slots__ = ()
    # arguments
    modules = "<module>"


class ListArguments(BaseArguments):
    """
    Arguments and options for the `list` sub-command.
    """
    def __init__(self, *args, **kwargs):
        super(ListArguments, self).__init__(*args, **kwargs)
        self._modules = None
        self.sub_usage = __doc__
        self._function = None
        return

    @property
    def function(self):
        """
        The `list` sub-command
        """
        if self._function is None:
            self._function = self.subcommands.list_plugins
        return self._function

    @property
    def modules(self):
        """
        List of external modules holding plugins
        """
        if self._modules is None:
            self._modules = self.sub_arguments[ListArgumentsConstants.modules]
        return self._modules

    def reset(self):
        """
        Resets the attributes to None
        """
        super(ListArguments, self).reset()
        self._modules = None
        return
# end ListArguments
