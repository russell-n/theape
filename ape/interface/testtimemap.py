
# python standard library
import unittest
import random
import string
from collections import defaultdict
from types import IntType, FloatType
from datetime import timedelta

# this package
from ape import BaseClass
from ape import ApeError
from timemap import RelativeTimeMap
from timemap import RelativeTimeMapGroups
from timemap import RelativeTime


EMPTY_STRING = ''
SPACE = ' '
MICRO = 10**6
RANDOM_MIN = random.randrange(-100, 0)
RANDOM_MAX = random.randrange(0, 100)


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
        expected = defaultdict(lambda : DEFAULT)
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



class TestRelativeTime(unittest.TestCase):
    """
    Tests the Relative Time class
    """
    def setUp(self):
        self.source = '5 Sec'
        self.relative = RelativeTime(self.source)
        self.time_map = RelativeTimeMap()
        return

    def test_constructor(self):
        """
        Does the RelativeTime class' constructor match the expectation? 
        """
        # is it setting the parameters?
        self.assertEqual(self.relative.source, self.source)

        # is it a child of BaseClass (so it has a logger)?
        self.assertIs(self.relative.__class__.__base__, BaseClass)

        # does it not require the source parameter?
        RelativeTime()
        return

    def test_get_number(self):
        """
        Does it get the number from a string?
        """
        self.relative.source = None
        with self.assertRaises(ApeError):
            self.relative.get_number(self.time_map.second_expression,
                                     RelativeTimeMapGroups.seconds)
        number = '3.2'
        source = number + ' sec'
        self.relative.source = source
        self.assertEqual(self.relative.get_number(self.time_map.second_expression,
                                                  RelativeTimeMapGroups.seconds),
                                                  number)
        with self.assertRaises(IndexError):
            self.relative.get_number(self.time_map.second_expression,
                                     'apeape')
        return

    def test_populate_fields(self):
        """
        Do the field get the right numbers?
        """
        weeks = 2
        days_int = 2
        days_frac = .4
        days = days_int + days_frac
        
        hours = 3.4

        minutes = 2.9

        seconds_int = 3
        seconds_frac = 0.2
        seconds = seconds_int + seconds_frac
        source = '{w} weeks {d} d {h} Hrs {m} Minutes {s} seconds'.format(h=hours,
                                                          m=minutes,
                                                          s=seconds,
                                                          d=days,
                                                          w=weeks)
        seconds = int(seconds_int + minutes * 60 + hours * 3600 + days_frac * 24 * 3600)
        microseconds = seconds_frac  * MICRO
        expected_days = weeks * 7 + days_int
        message = 'Source: {0}, Expected: {{0}}, Actual: {{1}}'.format(source)
        self.relative.source = source
        self.assertEqual(self.relative.days, expected_days, msg=message.format(expected_days,
                                                                          self.relative.days))
        self.assertEqual(self.relative.seconds, seconds, msg=message.format(seconds,
                                                                            self.relative.seconds))
        self.assertEqual(self.relative.microseconds, microseconds)
        return

    def test_populate_fields_extended(self):
        """
        Does it use the dateutil.relativedelta extensions to timedelta?
        """
        months = 1
        source = "{0} months".format(months)
        self.relative.source = source
        self.assertIn(self.relative.days, ( 28, 29, 30, 31))

        years = 2
        source = "{0} yrs".format(years)
        self.relative.source = source
        self.assertIn(self.relative.days, (365 * years, 366 * years))
        return

    def test_reset(self):
        """
        Does it reset the timedelta  to None?
        """
        self.relative.source = '4 d 3.2s'
        self.assertEqual(4, self.relative.days)
        self.assertEqual(3, self.relative.seconds)
        self.assertEqual(0.2 * MICRO, self.relative.microseconds)
        self.relative.reset()
        self.assertIsNone(self.relative.timedelta)
        return

    def test_attribute_errors(self):
        """
        Do the attributes raise ApeErrors if the timedelta hasn't been created?
        """
        self.relative.source = None
        with self.assertRaises(ApeError):
            self.relative.microseconds

        with self.assertRaises(ApeError):
            self.relative.seconds

        with self.assertRaises(ApeError):
            self.relative.days
        return

    def test_total_seconds(self):
        """
        Is total seconds the sum of the time values?
        """
        MINUTE = 60
        HOUR = 60 * MINUTE
        DAY = 24 * HOUR
        WEEK = 7 * DAY

        seconds = round(random.uniform(RANDOM_MIN,RANDOM_MAX), 1)
        minutes = round(random.uniform(RANDOM_MIN, RANDOM_MAX), 1)
        hours = round(random.uniform(RANDOM_MIN, RANDOM_MAX), 1)
        days = round(random.uniform(RANDOM_MIN, RANDOM_MAX), 1)
        weeks = round(random.uniform(RANDOM_MIN, RANDOM_MAX), 1)
        
        YEAR = 365 * DAY + minutes * MINUTE + hours * HOUR + days * DAY + weeks * WEEK + seconds
        LEAP_YEAR = YEAR + DAY
        
        self.relative.source = '1 year, {m} Min {h} H {s} SEc {d} days {w}wks'.format(m=minutes,
                                                                                      d=days,
                                                                                      w=weeks,
                                                                                      h=hours,
                                                                                      s=seconds)
        self.assertIn(self.relative.total_seconds(), (YEAR, LEAP_YEAR))
        self.relative.source = None
        
        with self.assertRaises(ApeError):
            self.relative.total_seconds()
        return

    def test_addition(self):
        """
        Does it add with other timedeltas?
        """
        seconds_0 = random.randrange(RANDOM_MIN, RANDOM_MAX)
        seconds_1 = random.randrange(RANDOM_MIN, RANDOM_MAX)
        self.relative.source = '{0}s'.format(seconds_0)
        other = timedelta(seconds=seconds_1)
        total = self.relative + other
        self.assertAlmostEqual(seconds_0 + seconds_1,
                               total.total_seconds())

        with self.assertRaises(ApeError):
            self.relative + seconds_1

        with self.assertRaises(ApeError):
            self.relative.source = None
            total = self.relative + other
        return

    def test_commutative_add(self):
        """
        Will it add if it's on the RHS?
        """
        seconds_0 = random.randrange(RANDOM_MIN, RANDOM_MAX)
        seconds_1 = random.randrange(RANDOM_MIN, RANDOM_MAX)
        self.relative.source = '{0}s'.format(seconds_0)
        other = timedelta(seconds=seconds_1)
        total = other + self.relative 
        self.assertAlmostEqual(seconds_0 + seconds_1,
                               total.total_seconds())

        return

    def test_subtraction(self):
        """
        Does it subtract other timedeltas?
        """
        seconds_0 = random.randrange(RANDOM_MIN, RANDOM_MAX)
        seconds_1 = random.randrange(RANDOM_MIN, RANDOM_MAX)
        self.relative.source = '{0}s'.format(seconds_0)
        other = timedelta(seconds=seconds_1)
        total = self.relative - other
        self.assertAlmostEqual(seconds_0 - seconds_1,
                               total.total_seconds())

        total = other - self.relative 
        self.assertAlmostEqual(seconds_1 - seconds_0,
                               total.total_seconds())

        with self.assertRaises(ApeError):
            self.relative - 1
        return

    def test_mulitplication(self):
        """
        Does it supoort multiplication by integers?
        """
        seconds_0 = random.randrange(RANDOM_MIN, RANDOM_MAX)
        multiplier = random.randrange(RANDOM_MIN, RANDOM_MAX)
        self.relative.source = '{0}s'.format(seconds_0)

        total = self.relative * multiplier
        self.assertAlmostEqual(seconds_0 * multiplier,
                               total.total_seconds())

        total = multiplier * self.relative 
        self.assertAlmostEqual(multiplier * seconds_0,
                               total.total_seconds())

        with self.assertRaises(ApeError):
            self.relative * None
        return

    def test_negation(self):
        """
        Does it negate the timedelta?
        """
        seconds_0 = random.randrange(RANDOM_MIN, RANDOM_MAX)
        self.relative.source = '{0}s'.format(seconds_0)

        total = -self.relative
        self.assertAlmostEqual(seconds_0 * -1,
                               total.total_seconds())

        total = +self.relative
        self.assertAlmostEqual(seconds_0,
                               total.total_seconds())

        return

    def test_abs(self):
        """
        Does the absolute value method work?
        """
        seconds_0 = random.randrange(RANDOM_MIN, RANDOM_MAX)
        self.relative.source = '{0}s'.format(seconds_0)

        total = abs(self.relative)
        # I don't really get what it's doing, no test here
        return

    def test_equality(self):
        """
        Does it return true if a timedelta with the same time is tested against it?
        """
        seconds_0 = random.randrange(RANDOM_MIN, RANDOM_MAX)
        self.relative.source = '{0}s'.format(seconds_0)
        other = timedelta(seconds=seconds_0)
        self.assertEqual(self.relative, other)
        return


if __name__ == '__main__':
    import pudb; pudb.set_trace()
    timemap = RelativeTimeMap()
    years = timemap.year_expression.search('5 Years').group('years')
    print timemap('-7260872.1      S')
