Iwconfig
========


This is a module to work with the ``iwconfig`` command. Although ``iwconfig`` can be used to configure as well as query wireless interfaces, in this case I'll just be using it to get information.

.. '






IwconfigEnum
------------

A holder of constants so that users of this code will have a reference for the names used in the regular expressions.

.. uml::

    IwconfigEnum : essid
    IwconfigEnum : mac_protocol
    IwconfigEnum : mode
    IwconfigEnum : frequency
    IwconfigEnum : access_point
    IwconfigEnum : bit_rate
    IwconfigEnum : tx_power
    IwconfigEnum : link_quality
    IwconfigEnum : signal_level
    IwconfigEnum : rx_invalid_nwid
    IwconfigEnum : rx_invalid_crypt
    IwconfigEnum : rx_invalid_frag
    IwconfigEnum : tx_excessive_retries
    IwconfigEnum : invalid_misc
    IwconfigEnum : missed_beacons




IwconfigExpressions
-------------------

The ``IwconfigExpressions`` holds the compiled regular expressions to tokenize the output of the ``iwconfig`` command.

.. module:: theape.parts.wifi.iwconfig
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




.. _ape-iwconfigquery:

IwconfigQuery
-------------

Notes
~~~~~

According to the current (December 13, 2013) Ubuntu 13.10 man-page:

   * *ESSID* identifies cells that are part of the same virtual network (all APs with the same ESSID)
   * *Access Point* is the specific AP within the virtual network that the node is associated with
   * *mode* can be one of:

      - *Ad-Hoc* (only one cell, no AP)
      - *Managed* (node cat connect to many APS (allows roaming))
      - *Master* (node acts as syncronization master or Access Point)
      - *Repeater* (forwards packets to other wireless nodes)
      - *Secondary* (acts as backup master/repeater)
      - *Monitor* (passively monitor all packets on the frequency (not associated with a cell))

   * *Bit Rate* is the speed at which bits are transmitted (user speed lower due to congestion and overhead)
   * *RTS Threshold* - threshold for  handshake to make sure channel is clear (helps with congestion )
   * *fragmentation* splits IP packet into smaller fragments to help with interference
   * *Rx invalid nwid* is count of packets with different ESSID. Detects adjacent network on the same frequency.
   * *Tx excessive retries* is the number of packets not delivered.
   * *Invalid misc* is the number of packets lost for other wireless operations
   * *Missed beacon* is number of periodic beacons from the AP missed. Usually indicates out of range.

The Model and API
~~~~~~~~~~~~~~~~~

.. uml::

   BaseClass <|-- IwconfigQuery
   IwconfigQuery o- IwconfigExpressions

.. module:: theape.parts.wifi.iwconfig
.. autosummary::
   :toctree: api

   IwconfigQuery
   IwconfigQuery.event_timer
   IwconfigQuery.output
   IwconfigQuery.command
   IwconfigQuery.essid
   IwconfigQuery.mac_protocol
   IwconfigQuery.mode
   IwconfigQuery.frequency
   IwconfigQuery.access_point
   IwconfigQuery.bit_rate
   IwconfigQuery.tx_power
   IwconfigQuery.link_quality
   IwconfigQuery.signal_level
   IwconfigQuery.rx_invalid_nwid
   IwconfigQuery.rx_invalid_crypt
   IwconfigQuery.rx_invalid_frag
   IwconfigQuery.tx_excessive_retries
   IwconfigQuery.invalid_misc
   IwconfigQuery.missed_beacons
   IwconfigQuery.__call__
   IwconfigQuery.__str__
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



