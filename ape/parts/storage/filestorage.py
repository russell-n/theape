
# python standard library
import os
import shutil
import datetime
import re
import copy

# this package
from base_storage import BaseStorage
#from ape import BaseClass
from ape import FILE_TIMESTAMP
from ape import ApeError
from ape.commoncode.code_graphs import module_diagram, class_diagram


DIGIT = r'\d'
ONE_OR_MORE = '+'
UNDERSCORE = '_'
FILENAME_SUFFIX = UNDERSCORE + DIGIT + ONE_OR_MORE
IN_PWEAVE = __name__ == '__builtin__'


if IN_PWEAVE:
    example_path = 'aoeu/snth'
    example_file = 'umma.gumma'
    
    
    # this is the part that should be part of the path property
    if not os.path.isdir(example_path):
        os.makedirs(example_path)
    for name in os.listdir('aoeu'):
        print name
    
    # this will be run multiple times, remove the example so it gets started fresh
    if os.path.isdir(example_path):
        shutil.rmtree(example_path)    


name = "test_{timestamp}.csv"
print name.format(timestamp=datetime.datetime.now().strftime(FILE_TIMESTAMP))


if IN_PWEAVE:
    # what's here?
    for name in (name for name in os.listdir(os.getcwd()) if name.endswith('txt')):
        print name
    
    name = "innagaddadavida.txt"
    path = os.getcwd()
    full_name = os.path.join(path, name)
    if os.path.exists(full_name):
        base, extension = os.path.splitext(name)
    
        digit = r'\d'
        one_or_more = '+'
        underscore = '_'
    
        suffix = underscore + digit + one_or_more
        expression = r"{b}{s}{e}".format(b=base,
                                          s=suffix,
                                            e=extension)
        regex = re.compile(expression)
        count = sum(1 for name in os.listdir(path) if regex.match(name))
        count = str(count + 1).zfill(4)
        name = "{b}_{c}{e}".format(b=base, c=count, e=extension)
    
    print name    
        


class FileStorage(BaseStorage):
    """
    A class to store data to a file
    """
    def __init__(self, path=None, timestamp=FILE_TIMESTAMP):
        """
        FileStorage constructor

        :param:

         - `path`: path to prepend to all files (default is current directory)
         - `timestamp`: strftime format to timestamp file-names
        """
        super(FileStorage, self).__init__()
        self._path = None
        self.path = path
        self.timestamp = timestamp
        self.closed = True
        return

    @property
    def file(self):
        return self._file
    
    @property
    def path(self):
        """
        The path to prepend to files (cwd if not set by client)
        """
        if self._path is None:
            self._path = os.getcwd()
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

    def safe_name(self, name):
        """
        Adds a timestamp if formatted for it, increments if already exists

        :param:

         - `name`: name for file (without path added)

        :return: unique name with full path
        """
        name = name.format(timestamp=datetime.datetime.now().strftime(self.timestamp))
        full_name = os.path.join(self.path, name)
        if os.path.exists(full_name):
            base, extension = os.path.splitext(name)


            expression = r"{b}{s}{e}".format(b=base,
                                             s=FILENAME_SUFFIX,
                                             e=extension)
            regex = re.compile(expression)
            count = sum(1 for name in os.listdir(self.path) if regex.match(name))
            count = str(count + 1).zfill(4)
            name = "{b}_{c}{e}".format(b=base, c=count, e=extension)
            full_name = os.path.join(self.path, name)
        return full_name

    def open(self, name):
        """
        Opens a file for writing

        :param:

         - `name`: a basename (no path) for the file

        :return: copy of self with file as open file and closed set to False
        """
        name = self.safe_name(name)
        self.logger.debug("Opening {0} for writing".format(name))
        opened = copy.copy(self)
        opened.name = name
        opened._file = open(name, 'w')
        opened.closed = False
        return opened

    def close(self):
        """
        Closes self.file if it exists, sets self.closed to True
        """
        if self.file is not None:
            self.file.close()
            self.closed = True
        return                    


if IN_PWEAVE:
    this_file = os.path.join(os.getcwd(), 'filestorage.py')
    module_diagram_file = module_diagram(module=this_file, project='filestorage')
    print ".. image:: {0}".format(module_diagram_file)



if IN_PWEAVE:
    class_diagram_file = class_diagram(class_name="FileStorage",
                                       filter='OTHER',
                                       module=this_file)
    print ".. image:: {0}".format(class_diagram_file)
