
# python standard library
import unittest

# third-party
try:
    from mock import MagicMock, mock_open, patch
except ImportError:
    pass    

# the ape
from ape.parts.storage.csvstorage import CsvDictStorage
from ape.parts.storage.filestorage import FileStorage
from ape import ApeError


class TestCsvStorage(unittest.TestCase):
    def setUp(self):
        #self.mocked_file = mock_open()
        self.patcher = patch('__builtin__.open')
        self.mocked_file = self.patcher.start()
        self.path = 'folder'
        self.headers = "able baker charley".split()
        self.path = 'cow'
        self.file_storage = FileStorage(path=self.path)
        self.storage = CsvDictStorage(storage=self.file_storage,
                                      headers=self.headers)
        return

    def tearDown(self):
        self.patcher.stop()
        return

    def test_constructor(self):
        """
        Does it take the expected fields?
        """
        storage = CsvDictStorage(path=self.path, headers=self.headers,
                                 storage=self.file_storage)        
        self.assertEqual(self.path, storage.path)
        self.assertEqual(self.headers, storage.headers)
        self.assertEqual(self.file_storage, storage.storage)
        return

    def test_bad_constructor(self):
        """
        Does it raise an error if neither path nor storage are given?
        """
        with self.assertRaises(ApeError):
            CsvDictStorage(headers=self.headers)

        with self.assertRaises(TypeError):
            # headers are required too
            CsvDictStorage(path=self.path)
            
        with self.assertRaises(TypeError):            
            CsvDictStorage(storage = self.file_storage)

        with self.assertRaises(TypeError):
            CsvDictStorage()
        return

    def test_storage_writerow(self):
        """
        Does it not write a header and then the row?
        """
        data = zip(self.headers, ('1', '2', '3'))
        self.storage.writerow(data)        
        return

    def test_open(self):
        """
        Does it open a file with the given filename?
        """
        name = 'aoeu'
        dict_writer = MagicMock()
        dict_writer_instance = MagicMock()
        storage = MagicMock()
        dict_writer.return_value = dict_writer_instance
        self.file_storage.open = MagicMock()
        opened = MagicMock()
        self.file_storage.open.return_value = opened
        
        with patch('csv.DictWriter', dict_writer):
            writer = self.storage.open(name)

            # did it open a file using the filename?
            self.file_storage.open.assert_called_with(name)

            # Did it create and store a DictWriter?
            self.assertEqual(writer.writer, dict_writer_instance)

            # Did it create the DictWriter using the opened file and headers?
            dict_writer.assert_called_with(opened,
                                           self.headers)

            # did it return a copy of itself?
            self.assertIsInstance(writer, CsvDictStorage)
        return        
