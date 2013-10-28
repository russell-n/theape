
# python standard library
import unittest
import shutil

# this package
from ape.parts.storage.filestorage import FileStorage


PATH = 'ape/call'
class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.storage = FileStorage('test')
        return

    def test_constructor(self):
        """
        Does it set up the name and the BaseStorage parent?
        """
        storage = FileStorage(PATH)
        self.assertEqual(PATH, storage.path)
        return
    
    def tearDown(self):
        shutil.rmtree(PATH)
        return        
