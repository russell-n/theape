The Argument Clinic
===================
.. currentmodule:: ape.interface.arguments

.. _argument-clinic:

This is the module that builds the command-line interface for the Ape. It uses the python `argparse <http://docs.python.org/2/library/argparse.html>`_ module. In particular it uses the :ref:`UbootKommandant <uboot-kommandant>` to provide methods for the ArgParser's `sub-command <http://docs.python.org/2.7/library/argparse.html#sub-commands>`_ interface.

.. superfluous '

.. uml::

   ArgumentClinic o- argparse.ArgumentParser
   ArgumentClinic o- UbootKommandant

.. autosummary::
   :toctree: api

   ArgumentClinic
   ArgumentClinic.args
   ArgumentClinic.__call__
   ArgumentClinic.add_arguments
   ArgumentClinic.add_subparsers

The ArgumentClinic uses sub-parsers to enable the use of :ref:`sub-commands <untersee-boot>`.




This is what the ``--help`` flag gives as of October 17, 2013 (Pweave hijacks the ArgumentParser so an example has to be generated separately):

.. literalinclude:: sample_help.txt

