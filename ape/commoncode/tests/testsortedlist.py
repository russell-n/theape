
# python standard library
import unittest
import random

# third-party
import numpy

# this package
from ape.commoncode.sortedlist import SortedList


class TestSortedList(unittest.TestCase):
    def setUp(self):
        self.collection = SortedList()
        self.source = range(0, 101, 10)
        random.shuffle(self.source)
        for item in self.source:
            self.collection.insort(item)
        return

    def test_constructor(self):
        """
        Does it build correctly?
        """
        return

    def test_insort(self):
        """
        Does it insert things in order?
        """
        self.assertNotEqual(self.source, self.collection)
        self.assertEqual(sorted(self.source), self.collection)
        return

    def test_percentile(self):
        """
        Does it get the item at the ith percentile?
        """
        self.assertEqual(min(self.collection), self.collection.percentile(0))
        self.assertEqual(50, self.collection.percentile(50))
        return
