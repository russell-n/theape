Iwconfig
========

This is a module to work with the ``iwconfig`` command. Although ``iwconfig`` can be used to configure as well as query wireless interfaces, in this case I'll just be using it to get information.

.. '



IwconfigEnum
------------

A holder of constants so that users of this code will have a reference for the names used in the regular expressions.



IwconfigExpressions
-------------------

The ``IwconfigExpressions`` holds the compiled regular expressions to tokenize the output of the ``iwconfig`` command.

.. currentmodule:: ape.parts.wifi.Iwconfig
.. autosummary::
   :toctree: api

   IwconfigExpressions.essid
   IwconfigExpressions.mac_protocol



.. uml::

   BaseClass <|-- IwconfigQuery 

.. currentmodule:: ape.parts.wifi.iwconfig
.. autosummary::
   :toctree: api

   IwconfigQuery
   IwconfigQuery.event_timer
   IwconfigQuery.output
   IwconfigQuery.command
   IwconfigQuery.essid
   IwconfigQuery.__call__
   IwconfigQuery.check_errors
   IwconfigQuery.close



Responsibilities
----------------

 * maintains the expressions needed to parse the output of the ``iwconfig`` command

 * issue command to connection

 * returns requested values from the iwconfig output

Collaborators
-------------

 * Connections

