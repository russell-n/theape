Testing the Storage Composite
=============================

I'm getting kind of worn out. I don't know how much testing I'll do, but at least I'll see if it will build and object.

::

    class TestStorageComposite(unittest.TestCase):
        def setUp(self):
            self.composite = StorageComposite()
            self.storage = MagicMock()
            return
    
        def test_constructor(self):
            self.assertIsNone(self.composite.open_storages)
            return
    
        def test_add(self):
            self.composite.add(self.storage)
            self.assertIn(self.storage, self.composite.storages)
            return
    
        def test_remove(self):
            storage = MagicMock()
            self.composite.add(self.storage)
            self.assertIn(self.storage, self.composite.storages)
            self.composite.remove(self.storage)
            self.assertNotIn(self.storage, self.composite.storages)
    
        def test_open(self):
            opened = MagicMock()
            self.storage.open = opened
            self.composite.add(self.storage)
            self.composite.open('ummagumma')
            opened.assert_called_with('ummagumma')
            
    

