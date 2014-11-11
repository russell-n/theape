TheWatcher
==========

This is a watcher for information. Whatever ``query`` passed into it has to match the list of ``fields``.

.. _ape-thewatcher:

TheWatcher Class
-----------------

Role
~~~~

    * Gets values from a query at timed-intervals
    * Sends values to storage
    * if threaded, runs in background

Collaborators
~~~~~~~~~~~~~

 * Query
 * Storage

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

storage
~~~~~~~

Previously, the storage was always assumed to be a file-like object. To try and make it more flexible, I'm going to start assuming that it instead takes a dictonary and handles it (the behavior is assomed to match the ``csv.DictWriter``).

.. '


