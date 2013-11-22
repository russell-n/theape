The Countdown
=============

The Countdown Timers are meant to be used by the composites and components to keep track of elapsed (and sometimes remaining) time. The :ref:`Time Tracker <ape-parts-countdown-timetracker>` is used to keep track of how long execution is taking. This is meant primarily for someone wanting to estimate future times by looking at past logs. The :ref:`CountDown Timer <ape-parts-countdown-countdowntimer>` also keeps track of execution time but is meant to also keep track of whether the composite should repeat or not (based on remaining repetitions or time).

Contents:

    * :ref:`TimeTracker <ape-parts-countdown-timetracker>`

    * :ref:`CountdownTimer <ape-parts-countdown-countdowntimer>`


.. currentmodule:: ape.parts.countdown.countdown



.. _ape-parts-countdown-timetracker:

The TimeTracker
---------------

Responsibilities
~~~~~~~~~~~~~~~~

The TimeTracker:

    * Tracks start time, stop time, elapsed times

    * Logs min, Q1, median, Q3, max elapsed times

    * Returns True when running and False when stopped at __call__

The Model
~~~~~~~~~

.. uml::

   BaseClass <|-- TimeTracker
   TimeTracker : Bool __call__()
   TimeTracker : start
   TimeTracker : elapsed_times
   TimeTracker : __init__(log_level)

.. currentmodule:: ape.parts.countdown.countdown
.. autosummary::
   :toctree: api

   TimeTracker.__init__
   TimeTracker.log
   TimeTracker.append
   TimeTracker.percentile
   TimeTracker.__call__

   


The expected way to use the TimeTracker is as a sentinal in a while loop::

   
   def run(self):
       # assumes self.t is a TimeTracker instance
       while self.t():
           time.sleep(1)
       return

This would append a timedelta of about 1 second to the TimeTracker's times array everytime ``run`` is called, and log the current elapsed time and the basic running statistics (which in this case shouldn't show any variance)


.. _ape-parts-countdown-countdowntimer:

The CountdownTimer
------------------

The CountdownTimer is an extension of the TimeTracker that takes a `repetitions` value and decrements it on each call, returning True until it is less than or equal to 0.

.. note:: Because I decrement after the start-time is set, this will always return True on the first call (it assumes you want at least one repetition).

.. uml::

   TimeTracker <|-- CountdownTimer
   CountdownTimer : __call__()

.. currentmodule:: ape.parts.countdown.countdown
.. autosummary::
   :toctree: api

   CountdownTimer

