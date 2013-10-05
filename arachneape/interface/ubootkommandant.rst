The UbootKommandant
===================
.. currentmodule:: arachneape.interface.ubootkommandant


The try-except Decorator
------------------------

Since this is a user-level class (it is part of the command-line interface), exceptions are caught and logged, rather than allowing the interpreter to dump the stack-trace (it still logs and displays the stack-trace). To make this simpler a decorator is used to catch `Exception`.

.. autosummary::
   :toctree: api

   try_except
   


.. _uboot-kommandant:
This is a holder of sub-commands for the :ref:`ArgumentClinic <argument-clinic>`.

.. uml::

   UbootKommandant
   UbootKommandant o-- QuarterMaster

.. autosummary::
   :toctree: api

   UbootKommandant
   UbootKommandant.help
   UbootKommandant.run
   UbootKommandant.fetch
   UbootKommandant.list
   UbootKommandant.test



