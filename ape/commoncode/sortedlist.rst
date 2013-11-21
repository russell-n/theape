Sorted List
===========

This is a Data Collection that extends the List ADT to have an `insort` method that will insert an item in sorted order. If `append` or other non-sorting methods are used then this will not do anything meaningful, but if only insort is used (or a `sort` is called after many appends), then the `insort` will maintain the ordering.

.. currentmodule:: bisect
.. autosummary::
   :toctree: api

   bisect
   bisect.insort

.. uml::
   
   SortedList -|> list
   SortedList : insort(item)
   SortedList : percentile(percentile)
   
I added the `percentile` method to get some statistics from this but it seems like this is going down a bad path so I'm stopping at that.

.. '
   

.. currentmodule:: ape.commoncode.sortedlist
.. autosummary::
   :toctree: api

   SortedList
   SortedList.insort
   SortedList.append
   SortedList.sort
   SortedList.percentile

