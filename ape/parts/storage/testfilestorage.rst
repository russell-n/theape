Testing The File Storage
========================

::

    snth
    
    

::

    class TestFileStorage(unittest.TestCase):
        def setUp(self):
            self.storage = FileStorage('test')
            return
    
        def test_constructor(self):
            """
            Does it set up the name and the BaseStorage parent?
            """
            name = 'ape'
            storage = FileStorage(name)
            self.assertEqual*(name, storage.name)
            self.assertEqual(BaseStorage, storage.__base__)
            return
    

