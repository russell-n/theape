
# python standard library
import unittest

# the ape
from theape.infrastructure.arguments.argumentbuilder import ArgumentBuilder
from theape.infrastructure.arguments.fetcharguments import Fetch
from theape.infrastructure.arguments.runarguments import Run
from theape.infrastructure.arguments.listarguments import List
from theape.infrastructure.arguments.checkarguments import Check
from theape.infrastructure.arguments.helparguments import Help

class TestArgumentBuilder(unittest.TestCase):
    def test_constructor(self):
        """
        Does it build?
        """
        builder = ArgumentBuilder(args=['fetch'])
        return

    def test_parse_args(self):
        """
        Does it work like argparse?
        """
        builder = ArgumentBuilder(args=['fetch'])
        args = builder()
        self.assertEqual(args.command, 'fetch')
        self.assertIsInstance(args, Fetch)

        builder.args = ['run']
        args = builder()
        self.assertIsInstance(args, Run)

        builder.args = ['list']
        args = builder()
        self.assertIsInstance(args, List)

        builder.args = ['check']
        args = builder()
        self.assertIsInstance(args, Check)

        builder.args = ['help']
        args = builder()
        self.assertIsInstance(args, Help)
        return