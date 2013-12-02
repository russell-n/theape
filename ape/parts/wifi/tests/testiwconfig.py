
# python standard library
import unittest
from StringIO import StringIO
import time

# third party
from mock import MagicMock

# this package
from ape.parts.wifi.iwconfig import IwconfigQuery
from ape import ApeError


source = open('iwconfig.txt').read()
source2 = source.replace('simio_claustro', 'great_ape_ape')


class TestIwconfig(unittest.TestCase):
    def setUp(self):
        self.interface = 'wlan2'
        self.connection = MagicMock()
        self.iwconfig = IwconfigQuery(interface=self.interface,
                                      connection=self.connection)
        return

    def test_constructor(self):
        """
        Does it build correctly?        
        """
        self.assertEqual(self.interface, self.iwconfig.interface)
        self.assertEqual(self.connection, self.iwconfig.connection)
        return

    def test_command(self):
        """
        Does it send the right command?
        """
        self.assertEqual('iwconfig wlan2', self.iwconfig.command)
        return

    def test_call(self):
        """
        Does it send the command and return the output?
        """
        self.connection.iwconfig.return_value = (None,
                                                 StringIO(source),
                                                 '')
        output = self.iwconfig()
        self.assertEqual(output, StringIO(source).readlines())
        return

    def test_check_errors(self):
        """
        Does it raise the ApeError if appropriate?
        """
        # non-existent intergface
        self.connection.iwconfig.return_value = (None, StringIO(source),
                                                 StringIO('wlan0      No such device'))
        self.assertRaises(ApeError, self.iwconfig)

        # non-wireless interface
        self.connection.iwconfig.return_value = (None, StringIO(source),
                                                 StringIO('wlan0      no wireless extensions.'))
        self.assertRaises(ApeError, self.iwconfig)

        # device doesn't have iwconfig
        # non-wireless interface
        self.connection.iwconfig.return_value = (None, StringIO(source),
                                                 StringIO('iwconfig:      command not found'))
        self.assertRaises(ApeError, self.iwconfig)
        return

    def test_output(self):
        """
        Does the output get set if checked after a certain time interval?
        """
        # two calls in rapid succession
        outputs = [(None, StringIO(source2),''),
                   (None, StringIO(source), '')]
        def side_effect(*args, **kwargs):
            return outputs.pop()
        self.connection.iwconfig.side_effect = side_effect
        self.assertEqual(self.iwconfig.output,
                         StringIO(source).readlines())
        self.assertEqual(self.iwconfig.output,
                         StringIO(source).readlines())

        # two calls outside the time
        outputs = [(None, StringIO(source2),''),
                   (None, StringIO(source), '')]
        def side_effect(*args, **kwargs):
            return outputs.pop()
        self.iwconfig._event_timer = None
        self.iwconfig.interval = 0
        self.connection.iwconfig.side_effect = side_effect
        self.assertEqual(self.iwconfig.output,
                         StringIO(source).readlines())
        time.sleep(0.1)
        self.assertEqual(self.iwconfig.output,
                         StringIO(source2).readlines())

        return
