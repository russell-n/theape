
# python standard library
import unittest

# this package
from timemap import RelativeTimeMap


class TestRelativeTimeMap(unittest.TestCase):
    def setUp(self):
        self.map = RelativeTimeMap()
        return

    def test_years(self):
        a = '5 Years'
        self.assertEqual('5', self.map.years(a))
        return
