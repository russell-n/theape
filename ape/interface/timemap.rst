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

.. _relative-time-map-model:

The UML Model
-------------

.. uml::

   RelativeTimeMap --|> BaseClass
   RelativeTimeMap o- dateutil.relativedelta.relativedelta

.. currentmodule:: ape.interface.timemap
.. autosummary::
   :toctree: api

   RelativeTimeMap


.. _relative-time-map-groups:

Relative Time Map Groups
------------------------

