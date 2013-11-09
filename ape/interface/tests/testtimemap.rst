Testing the Time Map
====================

This tests the RelativeTimeMap, RelativeTime, and AbsoluteTime.

Contents:

    * :ref:`Testing RelativeTimeMap <testing-relativetimemap>`
    
    * :ref:`Testing RelativeTime <testing-relativetime>`

    * :ref:`Testing AbsoluteTime <testing-absolutetime>`



.. currentmodule:: ape.interface.tests.testtimemap
.. autosummary::
   :toctree: api

   TestRelativeTimeMapExpressions.test_years
   TestRelativeTimeMapExpressions.test_months
   TestRelativeTimeMapExpressions.test_weeks
   TestRelativeTimeMapExpressions.test_days
   TestRelativeTimeMapExpressions.test_hours
   TestRelativeTimeMapExpressions.test_minutes
   TestRelativeTimeMapExpressions.test_seconds
   TestRelativeTimeMapExpressions.test_the_whole_shebang
   



.. _testing-relativetimemap:

Testing RelativeTimeMap
-----------------------

.. currentmodule:: ape.interface.tests.testtimemap
.. autosummary::
   :toctree: api

   TestRelativeTimeMapExpressions.test_years
   TestRelativeTimeMapExpressions.test_months
   TestRelativeTimeMapExpressions.test_weeks
   TestRelativeTimeMapExpressions.test_days
   TestRelativeTimeMapExpressions.test_hours
   TestRelativeTimeMapExpressions.test_minutes
   TestRelativeTimeMapExpressions.test_seconds
   TestRelativeTimeMapExpressions.test_the_whole_shebang



.. _testing-relativetime:

Testing RelativeTime
--------------------

.. autosummary::
   :toctree: api

   TestRelativeTime.test_constructor
   TestRelativeTime.test_get_number
   TestRelativeTime.test_populate_fields
   TestRelativeTime.test_populate_fields_extended
   TestRelativeTime.test_reset
   TestRelativeTime.test_attribute_errors
   TestRelativeTime.test_total_seconds
   TestRelativeTime.test_addition
   TestRelativeTime.test_datetime_add
   TestRelativeTime.test_commutative_add
   TestRelativeTime.test_subtraction
   TestRelativeTime.test_multiplication
   TestRelativeTime.test_negation
   TestRelativeTime.test_abs



.. _testing-absolutetime:

Testing AbsoluteTime
--------------------

Since the ``AbsoluteTime`` is using ``dateutil.parser.parse`` to do everything, this will just be a check to make sure it holds all the right attributes.

.. autosummary::
   :toctree: api

   TestAbsoluteTime.test_constructor
   TestAbsoluteTime.test_defaults
   TestAbsoluteTime.test_call
   TestAbsoluteTime.test_error

