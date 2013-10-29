Testing The File Storage
========================

::

    snth
    test_2013_10_28_05:38:31_PM.csv
    innagaddadavida.txt
    innagaddadavida_0001.txt
    innagaddadavida_0002.txt
    
    

::

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
    
        def test_write_error(self):
            storage = FileStorage(PATH)
            self.assertRaises(ApeError, storage.write, ('',))
            return
        
        def tearDown(self):
            shutil.rmtree(PATH)
            return        
    

