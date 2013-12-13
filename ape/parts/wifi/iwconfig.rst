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

.. currentmodule:: ape.parts.wifi.iwconfig
.. autosummary::
   :toctree: api

   IwconfigExpressions.essid
   IwconfigExpressions.mac_protocol
   IwconfigExpressions.mode
   IwconfigExpressions.frequency
   IwconfigExpressions.access_point
   IwconfigExpressions.bit_rate
   IwconfigExpressions.tx_power
   IwconfigExpressions.link_quality
   IwconfigExpressions.signal_level
   IwconfigExpressions.rx_invalid_nwid
   IwconfigExpressions.rx_invalid_crypt
   IwconfigExpressions.rx_invalid_frag
   IwconfigExpressions.tx_excessive_retries
   IwconfigExpressions.invalid_misc
   IwconfigExpressions.missed_beacons



.. uml::

   BaseClass <|-- IwconfigQuery
   IwconfigQuery o- IwconfigExpressions

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

