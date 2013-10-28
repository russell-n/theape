
# python standard library
import os
import shutil

# this package
from ape import BaseClass


example_path = 'aoeu/snth'
example_file = 'umma.gumma'

# this will be run multiple times, remove the example so it gets started fresh
if os.path.isdir(example_path):
    shutil.rmtree(example_path)

# this is the part that should be part of the path property
if not os.path.isdir(example_path):
    os.makedirs(example_path)
for name in os.listdir('aoeu'):
    print name


class FileStorage(BaseClass):
    """
    A class to store data to a file
    """
    def __init__(self, path=''):
        """
        FileStorage constructor

        :param:

         - `path`: path to prepend to all files
        """
        super(FileStorage, self).__init__()
        self._path = None
        self.path = path
        return

    @property
    def path(self):
        """
        The path to prepend to files
        """
        return self._path

    @path.setter
    def path(self, path):
        """
        Sets the path and creates the directory if needed
        """
        if not os.path.isdir(path):
            os.makedirs(path)
        self._path = path
        return
