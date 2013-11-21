
# python standard library
import unittest
from StringIO import StringIO

# third-party
try:
    from mock import mock_open, patch, call, MagicMock
except ImportError:
    pass

# this package
from ape.commoncode.index_builder import grab_headline


class TestIndexBuilder(unittest.TestCase):
    def setUp(self):
        self.headline = 'Hummus Cheese'
        self.test_string = '''


{0}
-------------

        Now is the winter of our discontent,
        Made glourious summer by this Son of York.
        '''.format(self.headline)
        self.open_mock = MagicMock(name='open_mock')
        self.file_mock = MagicMock(spec=file, name='file_mock')
        self.open_mock.return_value = self.file_mock
        self.file_mock.__enter__.return_value = StringIO(self.test_string)
        self.lines = {'ummagumma':StringIO('AAAA'),
                      'aoeu':StringIO('BBBB')}
        return

    def test_grab_headline(self):
        """
        Does it grab the headline?
        """        
        open_name = '__builtin__.open'
        with patch(open_name, self.open_mock):
            filename = 'ummagumma'
            grabbed = grab_headline(filename)
            try:
                self.open_mock.assert_called_with(filename)
            except AssertionError as error:
                print self.open_mock.mock_calls
                raise
            self.assertEqual(self.headline, grabbed)

        empty_string = """




        
        """
        self.file_mock.__enter__.return_value = StringIO(empty_string)
        with patch(open_name, self.open_mock):
            self.assertIsNone(grab_headline('aoeusnth'))
        return

