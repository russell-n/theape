# python standard library
import unittest
import socket

# third-party
from mock import patch, MagicMock

# this package
from ape.parts.storage.socketstorage import SocketStorage
from ape import ApeError


class TestSocketStorage(unittest.TestCase):
    def setUp(self):
        self.socket = MagicMock()
        self.storage = SocketStorage(self.socket)
        return

    def test_constructor(self):
        self.assertEqual(self.storage.file, self.socket)
        return

    def test_close(self):
        self.assertFalse(self.storage.closed)
        self.storage.close()
        self.socket.close.assert_called_with()
        self.assertTrue(self.storage.closed)
        return

    def test_read(self):
        output = ['a\n', 'b\n', '']
        self.storage._file = output
        actual = self.storage.read()
        self.assertEqual(output[0] + output[1], actual)
        return

    def test_read_timeout(self):
        self.socket.__iter__.side_effect = socket.timeout
        self.assertRaises(ApeError, self.storage.read)
        return

    def test_readline(self):
        expected = 'some line\n'
        self.socket.readline.return_value = expected
        actual = self.storage.readline()
        self.assertEqual(actual, expected)
        return

    def test_readilne_timeout(self):
        self.socket.readline.side_effect = socket.timeout
        actual = self.storage.readline()
        self.assertEqual(' ', actual)
# end class TestSocket    
