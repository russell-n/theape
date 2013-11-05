
# third party
import paramiko

# this package
from ape import BaseClass


class SSHConnection(BaseClass):
    def __init__(self, hostname, username, password=None, port=22,
                 compress=False, key_filename=None, timeout=None):
        """
        SSHConnection constructor

        :param:

         - `hostname`: the IP address or resolvable host-name
         - `username`: the login username
         - `password`: the password for the device (optional if public-keys set)
         - `port`: the port for the service
         - `compress`: if True, gzip the connection
         - `key_filename`: file-name or list of file-names for public-keys
         - `timeout`: seconds to wait for login before raising a socket.timeout         
        """
        super(SSHConnection, self).__init__()
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.compress = compress
        self.key_filename = key_filename
        self.timeout = timeout
        self._client = None
        self._lock = None
        return

    @property
    def client(self):
        """
        an SSHClient instance

        :rtype: SSHClient
        :return: SSH Client with the constructor's parameters
        """
        if self._client is None:
            self._client = paramiko.SSHClient(hostname=self.hostname,
                                              username=self.username,
                                              port=self.port,
                                              password=self.password,
                                              key_filename=self.key_filename,
                                              compress=self.compress,
                                              timeout=self.timeout)
        return self._client

    def sudo(self, command, password, timeout=None):
        """
        A convenience method to hide what's needed to run as root

        :param:

         - `command`: command to run (without the 'sudo' keyword)
         - `password`: the sudoer's password
         - `timeout`: Amount of time to wait for the connection to respond
        """
        stdin, stdout, stderr = self.client.exec_command("sudo {0}".format(command),
                                                         get_pty=True)
        stdin.write("{0}\n".format(password))
