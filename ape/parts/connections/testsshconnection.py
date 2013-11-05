"""
Some basic unittesting for the sshconnection
"""

# python standard library
import unittest

# third-party
from mock import MagicMock, patch

# this package
from ape.parts.connections.sshconnection import SSHConnection

class TestSSHConnection(unittest.TestCase):
    def setUp(self):
        self.hostname = 'snth'
        self.username = 'aoeu'
        self.password = 'zvwm'
        self.timeout = 10
        self.definition = MagicMock()
        self.client = MagicMock()
        self.definition.return_value = self.client
        
        self.connection = SSHConnection(hostname=self.hostname,
                                        username=self.username,
                                        password=self.password,
                                        timeout=self.timeout)
        return

    def test_constructor(self):
        hostname = 'aoeusnth'
        username = 'qjkzvwm'
        connection = SSHConnection(hostname=hostname,
                                   username=username)
        self.assertEqual(connection.hostname, hostname)
        self.assertEqual(connection.username, username)

        # required parameters
        self.assertRaises(TypeError, SSHConnection)

        # defaults
        self.assertEqual(22, connection.port)
        self.assertIsNone(connection.password)
        self.assertFalse(connection.compress)
        self.assertIsNone(connection.key_filename)
        self.assertIsNone(connection.timeout)
        return

    def test_client(self):
        with patch('paramiko.SSHClient', self.definition):
            sshclient = self.connection.client
            self.definition.assert_called_with(hostname=self.hostname,
                                               username=self.username,
                                               password=self.password,
                                               port=22,
                                               key_filename=None,
                                               compress=False,
                                               timeout=self.timeout)
            self.assertEqual(self.client, sshclient)
        return

    def test_sudo(self):
        """
        A convenience method to hide what's needed to run a command as root
        """
        i = MagicMock()
        o = MagicMock()
        e = MagicMock()
        self.client.exec_command.return_value = (i, o, e)
        with patch('paramiko.SSHClient', self.definition):
            command = 'alpha bravo'
            password = 'sntahoeu'
            timeout = 1
            ioe = self.connection.sudo(command=command,
                                 password=password,
                                 timeout=timeout)
        self.client.exec_command.assert_called_with('sudo {0}'.format(command), get_pty=True)
        i.write.assert_called_with(password + '\n')
        self.assertEqual(ioe.input, i)
        return
# end TestSSHConnection
