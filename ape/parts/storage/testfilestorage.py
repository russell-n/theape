
# python standard library
import unittest
import shutil
import os

# third party
try:
    from mock import MagicMock, mock_open, patch
except ImportError:
    pass    

# this package
from ape.parts.storage.filestorage import FileStorage
from ape.commoncode.errors import ApeError


PATH = 'ape/call'
class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.storage = FileStorage('test')
        self.mock_file = MagicMock()
        return

    def test_constructor(self):
        """
        Does it set up the name and the BaseStorage parent?
        """
        storage = FileStorage(PATH)
        self.assertEqual(PATH, storage.path)
        return

    def test_open(self):
        mocked = mock_open()
        name = 'ummagumma.txt'
        full_name = 'test/' + name
        storage = FileStorage('test/')
        with patch('__builtin__.open', mocked):
            self.assertTrue(storage.closed)
            opened = storage.open(name)
            self.assertEqual(full_name, opened.name)
            mocked.assert_called_with(full_name, 'w')
            self.assertFalse(opened.closed)
        return
        

    def test_write(self):
        self.storage.file = self.mock_file
        self.storage.write('alpha')
        self.mock_file.write.assert_called_with('alpha')
        
    def test_write_error(self):
        storage = FileStorage(PATH)
        self.assertRaises(ApeError, storage.write, ('',))
        return

    def test_writeline(self):
        self.storage.file = self.mock_file
        self.storage.writeline('beta')
        self.mock_file.write.assert_called_with('beta\n')
        return

    def test_writelines(self):
        text = 'gamma delta sigma rho'.split()
        self.storage.file = self.mock_file
        self.storage.writelines(text)
        self.mock_file.writelines.assert_called_with(text)
    
    def test_close(self):
        mock_file = MagicMock()
        self.storage.file = mock_file
        self.storage.closed = True
        self.storage.close()
        mock_file.close.assert_called_with()
        self.assertTrue(self.storage.closed)
        return
    
    def tearDown(self):
        if os.path.isdir(PATH):
            shutil.rmtree(PATH)
        return        
