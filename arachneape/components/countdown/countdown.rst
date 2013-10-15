The Countdown
=============

.. currentmodule:: arachneape.components.countdown.countdown
.. _countdown-class:


The CountDown keeyps track of elapsed time and estimates remaining time either by repetitions or total allowed time.

.. uml::

   CountDown -|> DummyClass

.. autosummary::
   :toctree: api

   CountDown
   CountDown.start_timer
   CountDown.next_iteration
   CountDown.remaining_time
   CountDown.remaining_iterations
   CountDown.elapsed_time

To start off it will only take expected iterations and estimate time-remaining based on time elapsed. 
   


