
# python standard library
import datetime
from datetime import timedelta

# third party
import numpy

# this package
from ape import BaseClass, ApeError


DEBUG = 'debug'
INFO = 'info'
STAT_STRING = 'Time Stats -- Min: {min}, Q1: {q1}, Med: {med}, Q3: {q3}, Max: {max}, Mean: {mean}, StD: {std}'
ELAPSED_STRING = 'Elapsed Time: {0}'
TOTAL_ELAPSED_STRING = '({0}) Elapsed Time: {1}'
MIN_PERCENTILE = 0
Q1_PERCENTILE = 25
MEDIAN_PERCENTILE = 50
Q3_PERCENTILE = 75
MAX_PERCENTILE = 100

CONTINUE = True
STOP = False
NOT_SET = None
DECREMENT = -1
FINISHED = 0
ANNIHILATE = None


class TimeTracker(BaseClass):
    """
    A tracker of elapsed time
    """
    def __init__(self, log_level=DEBUG):
        """
        :param: `log_level`: level at which to report elapsed times (default='debug')
        """
        super(TimeTracker, self).__init__()
        self._logger = None
        self.log_level = log_level
        self.start = None
        self._times = None
        self._log = None
        return

    @property
    def times(self):
        """
        collection of elapsed times
        """
        if self._times is None:
            self._times = []
        return self._times

    @times.setter
    def times(self, times):
        """
        :param: ``times`` - collection
        :postcondition: self._times set to times
        """
        self._times = times
        return

    @property
    def log(self):
        """
        The logger method indicated by the log_level

        :return: logger.debug or logger.info
        """
        if self._log is None:
            if self.log_level == INFO:
                self._log = self.logger.info
            elif self.log_level == DEBUG:
                self._log = self.logger.debug
            else:
                raise ApeError("Unknown log level: {0}".format(self.log_level))
        return self._log
        

    def append(self, item):
        """
        Appends the item to the times array

        :param:

         - `item`: item to append to self.times (a numpy array)

        :postcondition: self.times contains item
        """
        self.times = numpy.append(self.times, [item])
        return

    def percentile(self, percentile):
        """
        calculates the percentile (e.g. 50 gets the median (the 50% item))

        :return: value for percintile of self.times as a timedelta
        """
        return timedelta(seconds=numpy.percentile(self.times, percentile))

    def __call__(self):
        """
        The main interface - starts and stops (toggles) the timer

        :return: True if starting, False if stopping
        :postcondition: elapsed time logged and added to self.times
        """
        if self.start is None:
            self.start = datetime.datetime.now()            
            return True
        elapsed = datetime.datetime.now() - self.start
        # numpy can't handle timedeltas
        self.append(elapsed.total_seconds())
        self.start = None
        self.log(ELAPSED_STRING.format(elapsed))
        self.log(STAT_STRING.format(min=self.percentile(MIN_PERCENTILE),
                                    q1=self.percentile(Q1_PERCENTILE),
                                    med=self.percentile(MEDIAN_PERCENTILE),
                                    q3=self.percentile(Q3_PERCENTILE),
                                    max=self.percentile(MAX_PERCENTILE),
                                    mean=timedelta(seconds=numpy.mean(self.times)),
                                    std=timedelta(seconds=numpy.std(self.times))))
        return False


class CountdownTimer(TimeTracker):
    """
    A time-tracker that counts down
    """
    def __init__(self, repetitions=1, *args, **kwargs):
        """
        :param: ``repetitions``: number of calls to accept before stopping
        """
        super(CountdownTimer, self).__init__(*args, **kwargs)
        self.repetitions = repetitions
        self.last_time = None
        return

    def __call__(self):
        """
        The main interface. Each call re-starts the timer and decrements the repetitions

        :return: True if repetitions > 0, False otherwise
        """
        call_time = datetime.datetime.now()
        
        if self.start is NOT_SET:
            self.start = self.last_time = call_time
            return CONTINUE

        # convert to seconds so numpy can calculate statistics
        self.append((call_time - self.last_time).total_seconds())
        self.log_update(call_time - self.last_time)
        self.last_time = call_time

        self.repetitions += DECREMENT

        if self.repetitions <= FINISHED:
            self.log_update(call_time - self.start)
            self.start = NOT_SET
            self._times = ANNIHILATE
            return False
        return CONTINUE

    def log_update(self, elapsed):
        """
        Outputs to the log the most recent elapsed time information

        :param:

         - `elapsed`: timedelta
        """

        elapsed_string = ELAPSED_STRING.format(elapsed)
        self.log(elapsed_string)
        self.log(STAT_STRING.format(min=self.percentile(MIN_PERCENTILE),
                                    q1=self.percentile(Q1_PERCENTILE),
                                    med=self.percentile(MEDIAN_PERCENTILE),
                                    q3=self.percentile(Q3_PERCENTILE),
                                    max=self.percentile(MAX_PERCENTILE),
                                    mean=timedelta(seconds=numpy.mean(self.times)),
                                    std=timedelta(seconds=numpy.std(self.times))))
        return

