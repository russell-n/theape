
# python standard library
import cStringIO as StringIO

# this package
from clientbase import BaseClient
from theape.parts.dummy.dummy import DummyClass
from theape import BaseClass

COMMA = ','
TIMEOUT = 10

class FakeClient(BaseClass):
    """
    A fake client 
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor

        :param:

         - `hostname`: ip address or resolvable hostname.
         - `username`: the login name.
         - `timeout`: Time to give the client to connect
         - `port`: TCP port of the server
         - `kwargs`: anything else that the client can use will be passed in to it
        """
        super(FakeClient, self).__init__(**kwargs)
        self._client = None
        self.args = args
        self.kwargs = kwargs
        return

    @property
    def client(self):
        """
        The fake client to the device
        """
        if self._client is None:
            self._clinte = DummyClass(name='FakeClient',
                                        *self.args,
                                        **self.kwargs)
        return self._client

    def exec_command(self, *args, **kwargs):
        """
        The main interface with the client

        :param:

         - `command`: A string to send to the client.
         - `timeout`: Set non-blocking timeout.

        :rtype: tuple
        :return: stdin, stdout, stderr
        """
        self.client(*args, **kwargs)
        return StringIO.StringIO(''), StringIO.StringIO(''), StringIO.StringIO('')
        
    def close(self):
        """
        Closes and removes the client (if it exists)
        
        :postcondition: client's connection is closed and self._client is None                
        """
        if self._client is not None:
            self._client.close()
            self._client = None
        return
    
    def __str__(self):
        """
        creates the string representation
        :return: username, hostname, port, password in string
        """
        return str(self.no_op)

    def __getattr__(self, method):
        """
        A pass-through to the client for un-implemented methods.

        .. warning:: This can't go in the base-class
        """
        return getattr(self.client, method)
# end FakeClient