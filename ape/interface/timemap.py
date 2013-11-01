
# python standard library
import re

# this package
from ape import BaseClass
from ape.commoncode.oatbran import CharacterClass, Numbers, Group
from ape.commoncode.oatbran import CommonPatterns


class RelativeTimeMapGroups(object):
    __slots__ = ()
    years = 'years'


class RelativeTimeMap(BaseClass):
    """
    A converter from strings with relative times to seconds
    """
    def __init__(self):
        super(RelativeTimeMap, self).__init__()
        self._year_expression = None
        return

    @property
    def year_expression(self):
        """
        A compiled regex to match a year (only checks for y)
        """
        if self._year_expression is None:
            self._year_expression = re.compile(Group.named(name=RelativeTimeMapGroups.years,
                                                           expression=(Numbers.real)) +
                                                            CommonPatterns.optional_spaces +
                                                            CharacterClass.character_class('Yy')
                                                            )
        return self._year_expression                
