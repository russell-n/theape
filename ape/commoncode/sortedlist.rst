Sorted List
===========

This is a Data Collection that extends the List ADT to have an `insort` method that will insert an item in sorted order. If `append` or other non-sorting methods are used than this will not do anything meaningful, but if only insort is used or a `sort` is called after many appends, then the `insort` will maintain the ordering.

.. currentmodule:: bisect
.. autosummary::
   :toctree: api

   bisect
   bisect.insort

.. uml::
   
   SortedList -|> list
   SortedList : insort(item)



.. currentmodule:: ape.commoncode.sortedlist
.. autosummary::
   :toctree: api

   SortedList
   SortedList.insort

