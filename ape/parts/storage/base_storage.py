
# python standard library
from abc import ABCMeta, abstractproperty

# this package
from ape import BaseClass


class BaseStorage(BaseClass):
    """A base-class based on file-objects"""
    def __init__(self, name):
        """
        BaseStorage Constructor

        :param:

         - `name`: an identifier for the file
        """
        __metaclass__ = ABCMeta
        super(BaseStorage, self).__init__()
        self._logger = None
        self.name = name
        self._file = None
        return

    @abstractproperty   
    def file(self):
        """
        The file object
        """
        return

    def flush(self):
        """
        Flushes the file-buffer
        """
        self.file.flush()
        return
        

    def close(self):
        """
        Closes self.file
        """
        self.file.close()
        return
    
    def __str__(self):
        return "{0}: {1}".format(self.__class__.__name__,
                                 self.name)
# end BaseStorage    
