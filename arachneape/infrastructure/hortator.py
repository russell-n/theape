
# this package
from arachneape.commoncode.baseclass import BaseClass
from arachneape.components.countdown.countdown import CountDown
from arachneape.commoncode.strings import RESET, BLUE, BOLD, BOLD_THING

# this module
from theoperator import OperatorError


class TheHortator(BaseClass):
    """
    An Exhorter of Operations
    """
    def __init__(self, operations, countdown=None):
        """
        TheHortator Constructor

        :param:

         - `operations`: iterable collection of Operators
         - `countdown`: CountDown timer
        """
        super(TheHortator, self).__init__()
        self.operations = operations
        self._countdown = countdown        
        return

    @property
    def countdown(self):
        """
        A Countdown Timer
        """
        if self._countdown is None:
            self._countdown = CountDown(iterations=len(self.operations))
        return self._countdown

    def __call__(self):
        """
        The main interface -- starts operations
        """
        self.countdown.start()
        count_string = "{b}** Operation {{c}} of {{t}} **{r}".format(b=BOLD, r=RESET)
        remaining_string = BOLD_THING.format(thing="Estimated Time Remaining:")
        total_elapsed = BOLD_THING.format(thing='** Total Elapsed Time:')
        
        total_count = len(self.operations)
        for count, operation in enumerate(self.operations):
            self.logger.info(count_string.format(c=count+1, t=total_count))
            self.logger.info(remaining_string.format(value=self.countdown.remaining))
            try:
                operation()
            except OperatorError as error:
                self.logger.error(error)
        self.logger.info(total_elapsed.format(value=self.countdown.elapsed))
        return
# end TheHortator
