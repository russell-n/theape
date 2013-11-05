
# python standard library
import os
import socket

# this package
from base_storage import BaseStorage

#from ape import BaseClass
from ape import ApeError
from ape.commoncode.code_graphs import module_diagram, class_diagram


NEWLINE = '\n'
SPACE = ' '
EOF = ''
IN_PWEAVE = __name__ == '__builtin__'


class SocketStorage(BaseStorage):
    """
    A class to store data to a file
    """
    def __init__(self, file):
        """
        SocketStorage constructor

        :param:

         - `socket_file`: opened file-like socket-based object
        """
        super(SocketStorage, self).__init__()
        self._file = file
        self.closed = False
        return

    @property
    def file(self):
        """
        :return: opened file-like object
        """
        return self._file

    def readline(self):
        """
        Calls a single read-line returns a space (' ') if socket.timeout
        """
        try:
            return self.file.readline()
        except socket.timeout:
            self.logger.debug('socket timedout')
            return SPACE
        
    
    def read(self):
        """
        reads all the output and returns as a single string
        """
        try:        
            return "".join((line for line in self.file))
        except socket.timeout as error:
            self.logger.debug('socket timeout')
            raise ApeError('Socket Timed out')
        return

    def __iter__(self):
        """
        Traverses the file

        :yield: next line in the file (or ' ' (a space) if it times-out)
        """
        line = None
        while line != EOF:
            try:
                yield self.file.readline()
            except socket.timeout:
                self.logger.debug('socket timed out')
                yield SPACE
        return
    
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
