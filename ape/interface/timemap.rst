Time Maps
=========


.. _relative-time-map:

Relative Time Map
-----------------

The `RelativeTimeMap` maps strings of relative times to seconds. It tries to be as liberal as possible so there has to be a fair amount of certainty that the string is in fact a time and not something similar but different. '5 yolks' will match '5' years, for instance, and if that is not the desired behavior then something else has to do a check first to filter out bad strings.

It uses `dateutil <http://labix.org/python-dateutil>`_ to calculate everything but the seconds because dateutil will handle the ambiguous values like years (which have leap-years) and months which have 28, 29, 30, or 31 days.

Contents:

   * :ref:`The UML Class Model <relative-time-map-model>`

   * :ref:`Relative Time Map Group Names <relative-time-map-groups>`

   * :ref:`The RelativeTime class <ape-relative-time>`

.. _relative-time-map-model:

The UML Model
-------------

.. uml::

   RelativeTimeMap --|> BaseClass
   RelativeTimeMap : re.RegexObject year_expression
   RelativeTimeMap : re.RegexObject month_expression
   RelativeTimeMap : re.RegexObject week_expression
   RelativeTimeMap : re.RegexObject day_expression
   RelativeTimeMap : re.RegexObject hour_expression
   RelativeTimeMap : re.RegexObject minute_expression
   RelativeTimeMap : re.RegexObject second_expression      
   
.. currentmodule:: ape.interface.timemap
.. autosummary::
   :toctree: api

   RelativeTimeMap
   


.. _relative-time-map-groups:

Relative Time Map Groups
------------------------



.. _ape-relative-time:

The RelativeTime
----------------

This is an attempt to extend the `timedelta` with weeks, hours, and minutes. The original intention was to also allow months and years, requiring the use of the `dateutil` package, but at this point I can't see an immediate use for it, so I'll stop at weeks, since it doesn't need special cases the way months and years do.

.. '

.. uml::

   RelativeTime -|> BaseClass
   RelativeTime o-- RelativeTimeMap
   RelativeTime : __init__(source)
   RelativeTime : int weeks
   RelativeTime : int days
   RelativeTime : int hours
   RelativeTime : int minutes
   RelativeTime : int seconds
   RelativeTime : int microseconds
   RelativeTime : datetime.timedelta
   RelativeTime : float total_seconds

By and large the intention is to use this like a time-delta object but with extra fields, so the operators will be overloaded too.

.. autosummary::
   :toctree: api

   RelativeTime
   RelativeTime.time_map

