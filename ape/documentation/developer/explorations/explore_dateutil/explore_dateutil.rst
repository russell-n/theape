Exploring Dateutil's Relativedelta
==================================

The first thing that I want to use `dateutil` for is calculating seconds based on times. Dateutil doesn't appear to be set up for this so I'm going to use a hack to see if it gets close enough.



.. currentmodule:: dateutil.relativedelta
.. autosummary::
   :toctree: api

   relativedelta

Minutes
-------

The `relativetimedelta` is a time-delta object, so you can't get seconds directly, but you can get it by adding and subtracting the same time.

::

    time = datetime.datetime.now()
    minutes = 5
    expected = minutes * 60
    delta = relativedelta(minutes=minutes)
    actual = (time + delta - time).seconds
    print expected == actual
    

::

    True
    

