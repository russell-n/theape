Iwconfig
========

This is a module to work with the ``iwconfig`` command. Although ``iwconfig`` can be used to configure as well as query wireless interfaces, in this case I'll just be using it to get information.

.. '

.. currentmodule:: ape.parts.wifi.iwconfig
.. autosummary::
   :toctree: api

   IwconfigQuery



Responsibilities
----------------

 * maintains the expressions needed to parse the output of the ``iwconfig`` command

 * issue command to connection

 * returns requested values from the iwconfig output

Collaborators
-------------

 * Connections

