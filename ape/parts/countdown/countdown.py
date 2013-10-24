
# this package
from ape.parts.dummy.dummy import DummyClass


# python standard library
import datetime


class CountDown(DummyClass):
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
