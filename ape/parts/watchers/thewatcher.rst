TheWatcher
==========

This is a watcher for information. Whatever ``query`` passed into it has to match the list of ``fields``.

TheWatcher Class
-----------------

.. uml::

   BaseThreadClass <|-- TheWatcher
   TheWatcher o- Query
   TheWatcher o- EventTimer
   TheWatcher o- Storage
   TheWatcher : query
   TheWatcher : fields

.. currentmodule:: ape.parts.watchers.thewatcher
.. autosummary::
   :toctree: api

   TheWatcher
   TheWatcher.header
   TheWatcher.__call__
   TheWatcher.check_rep

query
~~~~~

The ``query`` parameter should be a built query object (e.g. :ref:`IwconfigQuery <ape-iwconfigquery>`). The main interface runs threaded so the connection that it holds has to be thread-safe.
   

fields
~~~~~~

The ``fields`` parameter should be a list of names that match the properties of the query object that should be checked for output. If you want the RSSI and bitrate from the ``IwconfigQuery``, for instance, you would pass in a list of ``['signal_level', 'bit_rate']`` for the fields.


