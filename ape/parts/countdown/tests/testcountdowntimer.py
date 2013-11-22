
# python standard library
import unittest
import random
from datetime import timedelta

# third-party
from mock import MagicMock, patch
import numpy

# this package
from ape.parts.countdown.countdown import CountdownTimer, INFO


class TestCountdownTimer(unittest.TestCase):
    def setUp(self):
        # patch datetime
        self.datetime_patch = patch('datetime.datetime')
        self.datetime = self.datetime_patch.start()
        self.log_level = INFO
        self.logger = MagicMock()        

        self.repetitions = random.randrange(100)
        self.timer = CountdownTimer(repetitions=self.repetitions, log_level=INFO)
        return

    def tearDown(self):
        """
        Stop the patches
        """
        self.datetime_patch.stop()
        return


    def test_constructor(self):
        """
        Does it build?
        """
        self.assertEqual(self.timer.repetitions, self.repetitions)
        self.assertEqual(self.timer.log_level, INFO)
        self.assertIsNone(self.timer.start)
        self.assertIsNone(self.timer.last_time)
        self.assertIsNone(self.timer._times)
        return

    def test_call(self):
        """
        Does it keep track of time for the right number of repetitions?
        """
        # first repetition
        now = first_now = timedelta(seconds=10)
        self.datetime.now.return_value = first_now

        self.assertTrue(self.timer())
        
        self.datetime.now.assert_called_with()              
        self.assertEqual(self.timer.start, first_now)
        self.assertEqual(self.timer.last_time, first_now)
        self.assertEqual(self.timer.repetitions, self.repetitions)

        for repetition in xrange(1, self.repetitions):
            now +=  first_now
            self.datetime.now.return_value = now
            self.assertTrue(self.timer())
            self.assertEqual((first_now).total_seconds(), self.timer.times[repetition-1])
            self.assertEqual(self.timer.last_time, now)
            self.assertEqual(self.timer.repetitions, self.repetitions - repetition)
            self.assertTrue(all(numpy.array([10.] * repetition) == self.timer.times))

        # last repetition
        now += first_now
        self.datetime.now.return_value = now
        self.assertFalse(self.timer())

        self.assertEqual(self.timer.last_time, now)
        self.assertEqual(0, self.timer.repetitions)

        self.assertIsNone(self.timer.start)
        self.assertIsNone(self.timer._times)
        return
