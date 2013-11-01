
# python standard library
import unittest
import random
import string

# third party


# this package
from timemap import RelativeTimeMap
from timemap import RelativeTimeMapGroups


class TestRelativeTimeMap(unittest.TestCase):
    def setUp(self):
        self.map = RelativeTimeMap()
        return
    
    def get_space(self):
        return ' ' * random.randrange(10)
    
    def get_number(self):
        return ''.join([''.join(random.sample(string.digits, random.randint(1, 10))) ,random.choice(['','.']),
                            ''.join(random.sample(string.digits, random.randint(1,10)))])
        
    def get_year(self):
        number = self.get_number()
        space = self.get_space()
        years = random.choice('y Y'.split()) + 'ears' 
        string = "{0}{1}{2}".format(number, space, years)
        return number, string

    def get_month(self):
        number = self.get_number()
        space = self.get_space()
        month = random.choice('m M'.split()) + 'month' + random.choice(('', 's'))
        string = "{0}{1}{2}".format(number, space, month)
        return number, string

    def test_years(self):
        number, a = self.get_year()
        self.assertEqual(number, self.map.year_expression.search(a).group(RelativeTimeMapGroups.years))
        return

    def test_months(self):
        number, months = self.get_month()
        self.assertEqual(number, self.map.month_expression.search(months)).group(RelativeTimeMapGroups.months)
        


if __name__ == '__main__':
    import pudb; pudb.set_trace()
    timemap = RelativeTimeMap()
    years = timemap.year_expression.search('5 Years').group('years')
    print years
