
# python standard library
import re

# this package
from ape import BaseClass
from ape.commoncode.oatbran import CharacterClass, Numbers, Group
from ape.commoncode.oatbran import CommonPatterns


ZERO = '0'
MICRO = 10**6


class RelativeTimeMapGroups(object):
    __slots__ = ()
    years = 'years'
    months = 'months'
    weeks = 'weeks'
    days = 'days'
    hours = 'hours'
    minutes = 'minutes'
    seconds = 'seconds'
# end RelativeTimeMapGroups    


class RelativeTimeMap(BaseClass):
    """
    A converter from strings with relative times to seconds
    """
    def __init__(self):
        super(RelativeTimeMap, self).__init__()
        self._year_expression = None
        self._month_expression = None
        self._week_expression = None
        self._day_expression = None
        self._hour_expression = None
        self._minute_expression = None
        self._second_expression = None
        return

    @property
    def year_expression(self):
        """
        A compiled regex to match a year (only checks for y)
        """
        if self._year_expression is None:
            self._year_expression = re.compile(Group.named(name=RelativeTimeMapGroups.years,
                                                           expression=Numbers.real) +
                                                            CommonPatterns.optional_spaces +
                                                            CharacterClass.character_class('Yy')
                                                            )
        return self._year_expression

    @property
    def month_expression(self):
        """
        A compiled regex to match a month (check for 'mo' only)
        """
        if self._month_expression is None:
            self._month_expression = re.compile(Group.named(name=RelativeTimeMapGroups.months,
                                                            expression=Numbers.real) +
                CommonPatterns.optional_spaces +
                CharacterClass.character_class('Mm') +
                CharacterClass.character_class('Oo'))
        return self._month_expression

    @property
    def week_expression(self):
        """
        A compiled regex to extract a number of weeks
        """
        if self._week_expression is None:
            self._week_expression = re.compile(Group.named(name=RelativeTimeMapGroups.weeks,
                                                           expression=Numbers.real) +
                                                           CommonPatterns.optional_spaces +
                                                           CharacterClass.character_class('Ww'))
        return self._week_expression

    @property
    def day_expression(self):
        """
        A compiled regex to extract the number of days
        """
        if self._day_expression is None:
            self._day_expression = re.compile(Group.named(name=RelativeTimeMapGroups.days,
                                                          expression=Numbers.real) +
                                                          CommonPatterns.optional_spaces +
                                                          CharacterClass.character_class('Dd'))
        return self._day_expression

    @property
    def hour_expression(self):
        """
        A compiled regex to extract the number of hours
        """
        if self._hour_expression is None:
            self._hour_expression = re.compile(Group.named(name=RelativeTimeMapGroups.hours,
                                                           expression=Numbers.real) +
                                                           CommonPatterns.optional_spaces +
                                                           CharacterClass.character_class('Hh'))
        return self._hour_expression

    @property
    def minute_expression(self):
        """
        A compiled regex to extract the number of minutes
        """
        if self._minute_expression is None:
            self._minute_expression = re.compile(Group.named(name=RelativeTimeMapGroups.minutes,
                                                             expression=Numbers.real) +
                                                             CommonPatterns.optional_spaces +
                                                             CharacterClass.character_class('Mm') +
                                                             CharacterClass.character_class('Ii'))
        return self._minute_expression

    @property
    def second_expression(self):
        """
        A compiled regex to extract the number of seconds
        """
        if self._second_expression is None:
            self._second_expression = re.compile(Group.named(name=RelativeTimeMapGroups.seconds,
                                                             expression=Numbers.real) +
                                                             CommonPatterns.optional_spaces +
                                                             CharacterClass.character_class('Ss'))
        return self._second_expression
#end class RelativeTimeMap


class RelativeTime(BaseClass):
    """
    A timedeltas extension
    """
    def __init__(self, source):
        """
        RelativeTime constructor

        :param:

         - `source`: A string with relative time in it (e.g. '1week 2 days 4.2 seconds')
        """
        super(RelativeTime, self).__init__()
        self.microseconds = 0
        self._time_map = None
        self._source = None
        self.source = source
        return

    @property
    def source(self):
        """
        :return: the source string
        """
        return self._source

    @source.setter
    def source(self, source):
        """
        sets the source and all the time values
        """
        self._source = source
        self.populate_fields()
        return
    
    @property
    def time_map(self):
        """
        A relative time map instance to parse the source.
        """
        if self._time_map is None:
            self._time_map = RelativeTimeMap()
        return self._time_map

    def integer_fraction(self, expression, group_name):
        """
        Gets the token from self._source using expression, converts to integer and fraction (mantissa)

        :return: quotient, remainder or 0,0 if expression doesn't match
        """
        match = expression.search(self._source)
        if match is not None:
            number = match.group(group_name)
            if '.' in number:
                integer, fraction = number.split('.')
                quotient = int(integer)
                if len(fraction):
                    remainder = int(fraction)
                else:
                    remainder = 0
            else:
                quotient, remainder = int(number), 0
            self.logger.debug('q,r = {0},{1} (source={2})'.format(quotient, remainder, number))
            return quotient, remainder
        self.logger.debug("{0} not found in {1}".format(expression, self._source))
        return 0,0 
        
    def populate_fields(self):
        """
        populates the time fields with values (e.g. self.minutes)
        """
        self.seconds, fraction = self.integer_fraction(self.time_map.second_expression, RelativeTimeMapGroups.seconds)
        self.microseconds = int(fraction * MICRO)
        return

# end class RelativeTime    
