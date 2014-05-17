
# python standard library
import unittest
import random
import string

# the ape
from ape.interface.arguments.helparguments import HelpArguments


class TestHelpArguments(unittest.TestCase):
    def setUp(self):
        self.args = ['help']
        self.arguments = HelpArguments(args=self.args)
        return
    
    def test_constructor(self):
        """
        Does it build correctly?
        """
        arguments = HelpArguments(args=['help'])
        self.assertFalse(arguments.trace)
        return

    def test_width(self):
        """
        Does it get the screen-width?
        """
        self.assertEqual(self.arguments.width, 80)

        self.arguments.reset()
        width = random.randint(0, 100)
        self.arguments.args = self.args + ['--width', '{0}'.format(width)]
        self.assertEqual(width, self.arguments.width)
        return

    def test_modules(self):
        """
        Does it get a list of plugin modules?
        """
        # default is an empty list
        self.assertEqual([], self.arguments.modules)

        self.arguments.reset()
        modules = ["".join([random.choice(string.letters) for letter in xrange(random.randrange(1, 10))]) for
                   module in xrange(random.randrange(10))]
        mod_options = "-m " + ' -m '.join(modules)
        self.arguments.args = self.args + mod_options.split()
        self.assertEqual(self.arguments.modules, modules)
        return

    def test_name(self):
        """
        Does it get the name of the plugin?
        """
        self.assertEqual('Ape', self.arguments.name)

        self.arguments.reset()
        name = ''.join([random.choice(string.letters) for letter in xrange(random.randrange(1, 10))])
        self.arguments.args = self.args + [name]
        self.assertEqual(name, self.arguments.name)
        return

    def test_whole_shebang(self):
        """
        Does it get modules, screen width and names?
        """
        width = random.randrange(1, 100)
        width_option = '-w {0}'.format(width)
        modules = ["".join([random.choice(string.letters) for letter in xrange(random.randrange(1, 10))]) for
                   module in xrange(random.randrange(10))]
        mod_options = "-m " + ' -m '.join(modules)
        name = ''.join([random.choice(string.letters) for letter in xrange(random.randrange(1, 10))])

        self.arguments.args = self.args + [width_option] + mod_options.split() + [name]
        self.assertEqual(width, self.arguments.width)
        self.assertEqual(modules, self.arguments.modules)
        self.assertEqual(name, self.arguments.name)
        return
