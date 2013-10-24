
# python standard library
from bisect import insort


class SortedList(list):
    """
    Extends the `list` built-in with `insort`
    """
    def __init__(self, *args, **kwargs):
        """
        Sorted List Constructor 
        """
        super(SortedList, self).__init__(*args, **kwargs)
        return

    def insort(self, item):
        """
        Inserts item into list in sorted order
        """
        insort(self, item)
        return


import unittest
import random


class TestSortedList(unittest.TestCase):
    def setUp(self):
        self.collection = SortedList()
        return

    def test_insort(self):
        test = [random.randrange(0, 100) for item in xrange(100)]
        for item in test:
            self.collection.insort(item)
        self.assertEqual(sorted(test), self.collection)
