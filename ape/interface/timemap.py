
# python standard library
import re

# this package
from ape import BaseClass
from ape.commoncode.oatbran import CharacterClass, Numbers, Group
from ape.commoncode.oatbran import CommonPatterns


ZERO = '0'


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

    def get_number(self, source, expression, groupname):
        """
        Gets the number-value from the source

        :param:

         - `source`: string with the time
         - `expression`: regex to search the string
         - `groupname`: named-group name to get from the match object

        :rtype: float        
        :return: number from source or '0'
        """
        try:
            return float(expression.search(source).groupdict(default=ZERO)[groupname])
        except AttributeError as error:
            self.logger.debug(error)
            self.logger.debug('Source: {0}'.format(source))
            self.logger.debug('Group: {0}'.format(groupname))
            return 0
    
    def __call__(self, source):
        """
        Converts the source string to seconds

        :param:

         - `source`: string with '<float> <unit>' pairs (e.g. '1 Hour 3 Min')

        :rtype: float
        :return: total seconds found in the source
        """
        seconds = self.get_number(source, self.second_expression, RelativeTimeMapGroups.seconds)
        minutes = self.get_number(source, self.minute_expression, RelativeTimeMapGroups.minutes)
        return seconds + minutes
#end class RelativeTimeMap
