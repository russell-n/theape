The Hortator
============


.. currentmodule:: arachneape.infrastructure.hortator
Class
-----

**TheHortator**

Responsibility
--------------

Drives the operators and keeps track of total running time.

Collaborators
-------------

 * :ref:`Operators <the-operator>`

 * :ref:`CountDown <count-down>`

.. uml::

   TheHortator -|> BaseClass
   TheHortator o- "1" CountDown
   TheHortator o- "+" TheOperator


.. autosummary::
   :toctree: api

   TheHortator
   TheHortator.__call__

