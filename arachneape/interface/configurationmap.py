
# python standard library
import ConfigParser
import glob
import os
from collections import OrderedDict, namedtuple

# this package
from arachneape.commoncode.baseclass import BaseClass
from arachneape.commoncode.code_graphs import module_diagram, class_diagram
from arachneape.commoncode.errors import ConfigurationError


DEFAULT = 'DEFAULT'
CONFIG_GLOB = 'config_glob'
IN_PWEAVE = __name__ == '__builtin__'


class ConfigurationMap(BaseClass):
    """
    A map from configuration files to data
    """
    def __init__(self, filename):
        """
        ConfigurationMap constructor

        :param:

         - `filename`: filename(s) to create configuration
        """
        super(ConfigurationMap, self).__init__()
        self.filename = filename        
        self._parser = None
        return

    @property
    def parser(self):
        """
        A SafeConfigParser instance
        """
        if self._parser is None:
            self._parser = ConfigParser.SafeConfigParser()
            self._parser.read(self.filename)
            if self._parser.has_option(DEFAULT, CONFIG_GLOB):
                for name in glob.iglob(self._parser.get(DEFAULT, CONFIG_GLOB)):
                    self._parser.read(name)
        return self._parser

    def get(self, section, option, optional=True, default=None):
        """
        Gets the option from the section as a string

        :param:

         - `section`: section within the config file
         - `option`: option within the section
         - `optional`: If true return default instead of raising error for missing option
         - `default`: what to return if optional and not found
        """
        try:
            return self.parser.get(section, option)
        except ConfigParser.NoOptionError as error:
            self.logger.debug(error)
        if optional:
            return default
        raise ConfigurationError('No Such Option -- section: {0} option: {1}'.format(section,
                                                                                     option))

    def get_type(self, cast, section, option, optional=False, default=None):
        """
        Gets a value and casts it

        :param:

         - `cast`: function to cast the value
         - `section`: section with value
         - `option`: option in section with value

        :return: value from section:option
        :raise: ConfigurationError if it can't be cast
        """
        try:
            return cast(self.get(section, option, optional, default))
        except ValueError as error:
            value = self.get(section,
                             option,
                             optional,
                             default)
            self.logger.error(error)

            output = 'Section: {0}, Option: {1}, Value: {2}'.format(section,
                                                                    option,
                                                                    value)
            self.logger.error(output)                                                                    
            raise ConfigurationError("cannot cast: {0} to {1}".format(value,
                                                                      cast))

        
    def get_int(self, section, option, optional=False, default=None):
        """
        gets the value as an integer

        :return: value from section:option
        :raise: ConfigurationError if it can't be cast
        """
        return self.get_type(int, section, option, optional, default)
        
    def get_float(self, section, option, optional=False, default=None):
        """
        gets the value as a float
        """
        return self.get_type(float, section, option, optional, default)

    def get_boolean(self, section, option, optional=False, default=None):
        """
        Gets a value and casts it to a boolean

        :param:

         - `cast`: function to cast the value
         - `section`: section with value
         - `option`: option in section with value

        :return: value from section:option
        :raise: ConfigurationError if it can't be cast
        """
        try:
            return self.parser.getboolean(section, option)
        except ConfigParser.NoOptionError as error:
            self.logger.debug(error)
            if optional:
                return default
            else:
                raise ConfigurationError('No Such Option -- section: {0} option: {1}'.format(section,
                                                                                             option))
        except ValueError as error:
            value = self.get(section,
                             option,
                             optional,
                             default)
            self.logger.error(error)

            output = 'Section: {0}, Option: {1}, Value: {2}'.format(section,
                                                                    option,
                                                                    value)
            self.logger.error(output)                                                                    
            raise ConfigurationError("cannot cast: {0} to boolean".format(value))

    # to make it look more like ConfigParser
    getint = get_int
    getfloat = get_float
    getboolean = get_boolean
    
    def get_list(self, section, option, optional=False, default=None, delimiter=','):
        """
        Gets the value and converts it to a list

        :return: value list with whitespace trimmed
        """
        values =  self.get(section, option, optional=False, default=None).split(delimiter)
        return [value.strip() for value in values]

    def get_tuple(self, section, option, optional=False, default=None, delimiter=','):
        """
        Gets the value and converts it to a list

        :return: value list with whitespace trimmed
        """
        return tuple(self.get_list(section, option, optional=False, default=None,
                                   delimiter=delimiter))

    def get_dictionary(self, section, option, optional=False, default=None,
                       delimiter=',', separator=':'):
        """
        converts a delimiter-separated line to a key:value based dictionary (values are strings)
        """
        line = self.get_list(section, option, optional=False, default=None,
                              delimiter=',')
        return dict(item.split(separator) for item in line)

    def get_ordered_dictionary(self, section, option, optional=False, default=None,
                               delimiter=',', separator=':'):
        """
        converts a delimiter-separated line to a key:value based dictionary (values are strings)
        """
        line = self.get_list(section, option, optional=False, default=None,
                              delimiter=',')
        return OrderedDict(item.split(separator) for item in line)

    def get_named_tuple(self, section, option, optional=False, default=None,
                               delimiter=',', separator=':', cast=str):
        """
        Converts a line to a named tuple (Like the get_dictionary but keys are properties)

        namedtuple(section, fields)

        :param:
        
         - `section`: section in config (used as name for namedtuple
         - `option`: with <field><delimiter><value><separator> <field><delimiter><value>
         - `optional`: if True, missing option returns default
         - `default`: if optional and no option, return this
         - `delimiter`: token to separate <field><value> pairs
         - `separator: token to separate each <field><value> pair
         - `cast`:  function to cast all values
        """
        line = self.get_list(section, option, optional=False, default=None,
                              delimiter=',')
        tokens = [token.split(separator) for token in line]
        fields = [token[0] for token in tokens]
        values = (cast(token[1]) for token in tokens)
        
        definition = namedtuple(section, fields)
        return definition(*values)

    @property
    def sections(self):
        """
        :return: section names other than DEFAULT
        """
        return self.parser.sections()

    def has_option(self, section, option):
        """
        :return: True if section has this option
        """
        return self.parser.has_option(section, option)

    def options(self, section, optional=False, default=None):
        """
        gets a list of option-names

        :param:

         - `section`: section-name in the configuration
        
        :return: options in section
        """
        try:
            return self.parser.options(section)
        except ConfigParser.NoSectionError as error:
            if optional:
                self.logger.debug(error)
                return DEFAULT
            raise
        return

    def items(self, section, optional=False, default=None):
        """
        Gets tuples of (option, value) pairs for section

        :return: tuples
        """
        try:
            return self.parser.items(section)
        except ConfigParser.NoSectionError as error:
            if optional:
                self.logger.debug(error)
                return default
            raise
        return

    @property
    def defaults(self):
        """
        the [DEFAULT] section

        :return: dict of default values        
        """
        return self.parser.defaults()
# end class ConfigurationMap    


#python standard-library
import unittest
from StringIO import StringIO

# third-party
from mock import MagicMock, patch, mock_open

config = StringIO('''
[DEFAULT]
config_glob = *.ini
''')

sub_config = StringIO('''
[ARACHNEAPE]
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
        self.assertEqual(self.config.get('ARACHNEAPE', 'umma'), 'gumma')
        self.assertIsNone(self.config.get('ARACHNEAPE', 'amma', optional=True))
        self.assertEqual(sorted(self.config.sections), 'ARACHNEAPE SUBConfig2'.split())
        self.assertEqual(sorted(self.config.options(SUBCONFIG2)), 'config_glob not_true ten x'.split())
        self.assertEqual(self.config.get_int(SUBCONFIG2, 'ten'), 10)
        with self.assertRaises(ConfigurationError):
            self.config.get_int(SUBCONFIG2, 'x')
        self.assertEqual(self.config.get_float(SUBCONFIG2, 'x'), 2.5)
        self.assertFalse(self.config.get_boolean(SUBCONFIG2, 'not_true'))
        self.assertEqual(self.config.get_list('ARACHNEAPE', 'alpha'), 'a b c'.split())
        self.assertEqual(self.config.get_tuple('ARACHNEAPE', 'alpha'), tuple('a b c'.split()))
        self.assertItemsEqual(self.config.get_dictionary('ARACHNEAPE', 'beta').keys(), 'a b'.split())
        self.assertItemsEqual(self.config.get_dictionary('ARACHNEAPE', 'beta').values(), 'x y'.split())
        self.assertItemsEqual(self.config.get_ordered_dictionary('ARACHNEAPE', 'gamma').keys(), 'z w'.split())
        named = self.config.get_named_tuple('ARACHNEAPE', 'gamma')
        self.assertEqual(named.z, 'q')
        return


if IN_PWEAVE:
    this_file = os.path.join(os.getcwd(), 'configurationmap.py')
    module_diagram_file = module_diagram(module=this_file, project='configurationmap')
    print ".. image:: {0}".format(module_diagram_file)


if IN_PWEAVE:
    class_diagram_file = class_diagram(class_name="ConfigurationMap",
                                       filter='OTHER',
                                       module=this_file)
    print ".. image:: {0}".format(class_diagram_file)
