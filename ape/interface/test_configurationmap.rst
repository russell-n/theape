Testing the ConfigurationMap
============================

::

    #python standard-library
    import unittest
    from StringIO import StringIO
    
    # third-party
    from mock import MagicMock, patch, mock_open
    
    # this package
    from configurationmap import ConfigurationMap
    from ape.commoncode.errors import ConfigurationError
    

::

    config = StringIO('''
    [DEFAULT]
    config_glob = *.ini
    ''')
    
    sub_config = StringIO('''
    [APE]
    umma=gumma
    alpha = a, b, c
    beta = a:x, b:y
    gamma = z:q, w:r
    ''')
    
    sub_config_2 = StringIO('''
    [SUBConfig2]
    ten = 10
    x = 2.5
    not_true = False
    ''')
    
    SUBCONFIG2 = 'SUBConfig2'
    
    configs = [config, sub_config, sub_config_2]
    def config_effect(name):
        return configs.pop(0)
    
    

::

    class TestConfigurationMap(unittest.TestCase):
        def setUp(self):
            self.filename = 'filename.ini'
            self.config = ConfigurationMap(self.filename)
            self.config._logger = MagicMock()
            return 
            
        def test_constructor(self):
            self.assertEqual(self.filename, self.config.filename)
            return
    
        def test_parser(self):
            iglob = MagicMock()
            m = mock_open()
            m.side_effect = config_effect
            iglob.return_value = ['ape.ini', 'beep.ini']
            with patch('__builtin__.open', m):
                with patch('glob.iglob', iglob):
                    parser = self.config.parser
            self.assertTrue(self.config.has_option('DEFAULT', 'config_glob'))
            iglob.assert_called_with('*.ini')
            self.assertEqual(self.config.get('APE', 'umma'), 'gumma')
            self.assertIsNone(self.config.get('APE', 'amma', optional=True))
            self.assertEqual(sorted(self.config.sections), 'APE SUBConfig2'.split())
            self.assertEqual(sorted(self.config.options(SUBCONFIG2)), 'config_glob not_true ten x'.split())
            self.assertEqual(self.config.get_int(SUBCONFIG2, 'ten'), 10)
            with self.assertRaises(ConfigurationError):
                self.config.get_int(SUBCONFIG2, 'x')
            self.assertEqual(self.config.get_float(SUBCONFIG2, 'x'), 2.5)
            self.assertFalse(self.config.get_boolean(SUBCONFIG2, 'not_true'))
            self.assertEqual(self.config.get_list('APE', 'alpha'), 'a b c'.split())
            self.assertEqual(self.config.get_tuple('APE', 'alpha'), tuple('a b c'.split()))
            self.assertItemsEqual(self.config.get_dictionary('APE', 'beta').keys(), 'a b'.split())
            self.assertItemsEqual(self.config.get_dictionary('APE', 'beta').values(), 'x y'.split())
            self.assertItemsEqual(self.config.get_ordered_dictionary('APE', 'gamma').keys(), 'z w'.split())
            named = self.config.get_named_tuple('APE', 'gamma')
            self.assertEqual(named.z, 'q')
            return
    





