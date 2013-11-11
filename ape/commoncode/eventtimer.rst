EventTimer
==========

Contents:

    * :ref:`The EventTimer <ape-event-timer>`

    * :ref:`The Wait Decorator <ape-wait-decorator>`



.. _ape-event-timer:

The Event Timer
---------------

An EventTimer will block if you try to make a new request too soon (too soon being something that needs to be empirically determined by the user). It was originally created to prevent calls to a (slow) AP's http server from trying `GET` requests too frequently, as that caused the server to timeout. I think that it will be more useful here as a way to provide even intervals to things that have to make calls at certain times (e.g. code that watches a proc-file).

.. '

.. uml::

   EventTimer o- threading.Event
   EventTimer o- threading.Timer
   EventTimer -|> BaseClass
   EventTimer : __init__(event, seconds)   

.. currentmodule:: ape.commoncode.eventtimer
.. autosummary::
   :toctree: api

   EventTimer
   EventTimer.event
   EventTimer.timer
   EventTimer.set_event
   EventTimer.start
   EventTimer.clear
   EventTimer.wait



A Class Diagram
~~~~~~~~~~~~~~~

An auto-generated class diagram.

.. image:: EventTimer.png


.. _ape-wait-decorator:

The ``wait`` Decorator
----------------------

To make using the ``EventTimer`` easier, you can us the ``wait`` decorator. What it does:

    #. Call event.wait in case a previous timer is still running

    #. Clear the event

    #. Call the decorated method

    #. Start the timer

Basic Use::

   @wait
   def do_something(self):
       # do something here after the event-timer expires
       return

.. warning:: This is a method decorator -- it assumes the object it belongs to has a :ref:`timer <ape-event-timer>` property.

.. autosummary::
   :toctree: api

   wait
   


Module Diagram
--------------

A module diagram for this module.

.. image:: classes_eventtimer.png


An Example
----------

As a basic example, suppose you want to print 'Able was I ere I saw Elba' every second. You could do something like this::

    class Napolean(object):
        def __init__(self):
            self.timer = EventTimer(seconds=1)
            

        @wait
        def __call__(self):
            print 'Able was I ere I saw Elba'
            return

And this would print the palindrome with 1 second pauses in between::

    speak = Napolean()
    speak()

