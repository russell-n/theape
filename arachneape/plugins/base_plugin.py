
# python standard library
from abc import ABCMeta, abstractmethod, abstractproperty

# this package 
from arachneape.baseclass import BaseClass


class BasePlugin(BaseClass):
    """
    An abstract base-class for plugins
    """
    __metaclass__ = ABCMeta
    def __init__(self, configuration=None):
        super(BasePlugin, self).__init__()
        self._logger = None
        self._help = None
        self._fetch = None
        self._product is None
        return

    @abstractproperty
    def help(self):
        """
        A help string for this plugin
        """
        return

    @abstractproperty
    def product(self):
        """
        The plugin (BaseProduct implementation)
        """
        return

    @abstractproperty    
    def fetch(self):
        """
        Get sample config-file snippet required by this plugin
        """
        return
# end class BasePlugin                
