The Event Timer
===============





The EventTimer Class
--------------------

.. module:: theape.parts.eventtimer
.. autosummary::
   :toctree: api

   EventTimer
   EventTimer.event
   EventTimer.set_event
   EventTimer.start
   EventTimer.clear
   EventTimer.wait
   EventTimer.close
   EventTimer.is_set

   




The Wait (decorator) Function
-----------------------------

.. autosummary::
   :toctree: api

   wait

The ``wait`` decorator expects that it is decorating a method in a class that has an EventTimer object as a ``timer`` property (it references ``self.timer``).



