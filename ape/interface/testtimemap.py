
# python standard library
import unittest
import random
import string
from collections import defaultdict

# third party


# this package
from timemap import RelativeTimeMap
from timemap import RelativeTimeMapGroups


EMPTY_STRING = ''
SPACE = ' '


class TestRelativeTimeMapExpressions(unittest.TestCase):
    def setUp(self):
        self.map = RelativeTimeMap()
        self.upper_limit = random.randrange(10, 100)
        return
    
    def get_space(self):
        """
        :return: random amount of spaces (0..upper_limit)
        """
        return SPACE * random.randrange(self.upper_limit)

    def get_natural(self):
        """
        :return: a positive integer with no leading zeros
        """
        digits = random.randrange(self.upper_limit)
        prefix = random.choice('123456789')
        return prefix + EMPTY_STRING.join([random.choice(string.digits) for digit in xrange(digits)])
    
    def get_number(self):
        """
        :return: random integer or real number
        """
        return EMPTY_STRING.join([self.something_or_nothing('-'),
                                  self.get_natural(),
                                  self.something_or_nothing('.'),
                                  self.get_natural()])

    def get_value(self, suffix):
        """
        Creates a string with a random number, random number of spaces, and the suffix

        :param:

         - `suffix`: the suffix to add to the string (e.g. 'months')
        
        :return: get_number(), string of <number><space><suffix>
        """
        number = self.get_number()
        space = self.get_space()
        return number,"{0}{1}{2}".format(number, space, suffix)

    def something_or_nothing(self, something):
        """
        :return: something or empty string
        """
        return random.choice((EMPTY_STRING, something))

    def upper_or_lower(self, thing):
        """
        :return: upper or lowercase version of thing
        """
        if random.randrange(2):
            return thing.lower()
        return thing.upper()

    def plural_or_singular(self, thing):
        """
        :return: thing with or without 's'
        """
        return thing + self.something_or_nothing('s')

    def get_number_value(self, prefix, suffix):
        """
        :return: number, string with number-spaces-prefix-suffix
        """
        string = (self.upper_or_lower(prefix) +
                 self.something_or_nothing(self.plural_or_singular(suffix)))
        return self.get_value(string)
       
    def get_year(self):
        """
        :return: expected years, string to search
        """
        return self.get_number_value('y', 'ear')

    def get_month(self):
        """
        :return: expected number of months to find, string to search for months
        """
        return  self.get_number_value(self.upper_or_lower('m') + self.upper_or_lower('o'),
                                      'nth')
    def get_minutes(self):
        """
        :return: expected number of minutes, string to search for minutes
        """
        return self.get_number_value(self.upper_or_lower('m') + self.upper_or_lower('i'),
                                     'nute')
    def get_weeks(self):
        """
        :return: expected weeks, string to search for weeks
        """
        return self.get_number_value('w', 'eek')

    def get_days(self):
        """
        :return: expected days, string to search for days
        """
        return self.get_number_value('d', 'ay')

    def get_hours(self):
        """
        :return: expected hours, string to search for hours
        """
        return self.get_number_value('h', 'our')

    def get_seconds(self):
        """
        :return: expected seconds, string to search for seconds
        """        
        return self.get_number_value('s', 'econd')

    def try_assert_equal(self, getter, expression, group):
        """
        checks if the expression gets the group-value from the source

        :param:

         - `getter`: method to get number, source tuple (e.g. get_years)
         - `expression`: regular expression to search the source string
         - `group`: name of the named group expected in the regex match
        """
        try:
            number, source = getter()
            self.assertEqual(number, expression.search(source).group(group))
        except IndexError as error:
            print error
            print "Expected: {0}".format(number)
            print "Source: {0}".format(source)
            print "Expression: {0}".format(expression)
            print "Group: {0}".format(group)
            raise
        return

    def try_assert_almost_equal(self, getter, converter):
        """
        Checks if the map's call will get the correct number of seconds

        :param:

         - `getter`: method to get the name,source (e.g. get_year)
         - `converter`: method to convert the number to expected seconds
        """
        number, source = getter()
        expected = converter(number)
        actual = self.map(source)
        self.assertAlmostEqual(expected,
                               actual,
                               msg="Expected: {0} Actual: {1} Source: {2}".format(expected,
                                                                                  actual,
                                                                                  source))
        return

    def test_years(self):
        """
        Does the map's year expression extract the year?
        """
        self.try_assert_equal(self.get_year, self.map.year_expression, RelativeTimeMapGroups.years)
        return

    def test_months(self):
        """
        Does the map's month expression extract the month (and not minutes)?
        """
        self.try_assert_equal(self.get_month, self.map.month_expression, RelativeTimeMapGroups.months)
        number, minutes = self.get_minutes()
        self.assertIsNone(self.map.month_expression.search(minutes))
        return

    def test_weeks(self):
        """
        Does the map's week expression extract the number of weeks?
        """
        self.try_assert_equal(self.get_weeks, self.map.week_expression, RelativeTimeMapGroups.weeks)
        return

    def test_days(self):
        """
        Does the map's day expression extract the number of days?
        """
        self.try_assert_equal(self.get_days, self.map.day_expression, RelativeTimeMapGroups.days)
        return

    def test_hours(self):
        """
        Does the map's hour expression extract the number of hours?
        """
        self.try_assert_equal(self.get_hours,
                              self.map.hour_expression,
                              RelativeTimeMapGroups.hours)
        return

    def test_minutes(self):
        """
        Does the map's minute expression extract the number of minutes?
        """
        self.try_assert_equal(self.get_minutes,
                              self.map.minute_expression,
                              RelativeTimeMapGroups.minutes)

    def test_seconds(self):
        """
        Does the map's seconds expression extract the number of seconds?
        """
        self.try_assert_equal(self.get_seconds,
                              self.map.second_expression,
                              RelativeTimeMapGroups.seconds)

    def test_the_whole_shebang(self):
        """
        Does it extract the tokens separately?
        """
        time_source = {RelativeTimeMapGroups.years:self.get_year,
                       RelativeTimeMapGroups.months:self.get_month,
                       RelativeTimeMapGroups.weeks:self.get_weeks,
                       RelativeTimeMapGroups.days:self.get_days,
                       RelativeTimeMapGroups.hours:self.get_hours,
                       RelativeTimeMapGroups.minutes:self.get_minutes,
                       RelativeTimeMapGroups.seconds:self.get_seconds}
        expressions = {RelativeTimeMapGroups.years:self.map.year_expression,
                       RelativeTimeMapGroups.months:self.map.month_expression,
                       RelativeTimeMapGroups.weeks:self.map.week_expression,
                       RelativeTimeMapGroups.days:self.map.day_expression,
                       RelativeTimeMapGroups.hours:self.map.hour_expression,
                       RelativeTimeMapGroups.minutes:self.map.minute_expression,
                       RelativeTimeMapGroups.seconds:self.map.second_expression}

        key_count = random.randint(1, len(time_source.keys()))
        random_keys = random.sample(time_source.keys(), key_count)
        random.shuffle(random_keys)
        DEFAULT = '0'
        expected = defaultdict(lambda : '0')
        sources = []

        for key in random_keys:
            number, source = time_source[key]()
            expected[key] = number
            sources.append(source)
        single_source = random.choice((EMPTY_STRING, SPACE)).join(sources)
        for key in random_keys:
            value = expressions[key].search(single_source).groupdict(default=DEFAULT)[key]
            self.assertEqual(expected[key], value)
        return

    def test_seconds_conversion(self):
        """
        Does the __call__ return a float matching the seconds?
        """
        self.try_assert_almost_equal(self.get_seconds,
                                     float)
        return

    def test_minutes_conversion(self):
        """
        Does the __call__ return a float converting the minutes to seconds?
        """
        self.try_assert_almost_equal(self.get_minutes,
                                     lambda x: float(x) * 60)
        return        


if __name__ == '__main__':
    import pudb; pudb.set_trace()
    timemap = RelativeTimeMap()
    years = timemap.year_expression.search('5 Years').group('years')
    print timemap('-7260872.1      S')
