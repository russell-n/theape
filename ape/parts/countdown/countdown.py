
# python standard library
import datetime
from datetime import timedelta

# third party
import numpy

# this package
from ape import BaseClass, ApeError


DEBUG = 'debug'
INFO = 'info'
STAT_STRING = 'Min: {min}, Q1: {q1}, Med: {med}, Q3: {q3}, Max: {max}, Mean: {mean}, StD: {std}'
ELAPSED_STRING = 'Elapsed: {0}'


class TimeTracker(BaseClass):
    """
    A tracker of elapsed time
    """
    def __init__(self, log_level=DEBUG):
        """
        TimeTracker constructor

        :param:

         -  `log_level`: level at which to report elapsed times
        """
        super(TimeTracker, self).__init__()
        self.log_level = log_level
        self.start = None
        self.times = []
        self._log = None
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
        self.log(STAT_STRING.format(min=self.percentile(0),
                                    q1=self.percentile(24),
                                    med=self.percentile(50),
                                    q3=self.percentile(75),
                                    max=self.percentile(100),
                                    mean=timedelta(seconds=numpy.mean(self.times)),
                                    std=timedelta(seconds=numpy.std(self.times))))
        return False


class CountDown(BaseClass):
    """
    A countdown timer
    """
    def __init__(self, iterations, *args, **kwargs):
        """
        CountDown Constructor

        :param:

         - `iterations`: Number of expected iterations.
        """
        super(CountDown, self).__init__(*args, **kwargs)
        self.iterations = iterations
        self.iteration = 0
        return

    @property
    def time_remaining(self):
        """
        An estimate of the time remaining
        """
        return self.iterations - self.iteration

    def start_timer(self):
        """
        Sets the start_time and lap_start_time to now
        """
        self.start_time = datetime.datetime.now()
        self.lap_start_time = self.start_time
        return

    def next_iteration(self):
        """
        Increments the iterations and saves the lap-time
        """
        self.iteration += 1
        return
# end class CountDown


# python standard library
import unittest


class TestCountDown(unittest.TestCase):
    def setUp(self):
        self.iterations = 4
        self.counter = CountDown(iterations=self.iterations)
        return

    def test_next_iteration(self):
        """
        Does it increment the iteration
        """
        self.assertEqual(self.iterations, self.counter.iterations)
        for value in xrange(self.iterations):
            self.counter.next_iteration()
            self.assertEqual(value+1, self.counter.iteration)
        self.assertEqual(0, self.counter.time_remaining)
        return
