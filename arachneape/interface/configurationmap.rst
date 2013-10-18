The Configuration Map
=====================

.. _configuration-map:
The `Configuration Map` maps a configuration-file-name to data. It extends the `ConfigParser` to have more data-types (and allow missing values).

ConfigParser Exceptions
-----------------------

These are the `ConfigParser` Exceptions that I will handle in the `ConfigurationMap`.

.. currentmodule:: ConfigParser
.. autosummary::
   :toctree: api

   ConfigParser.Error
   ConfigParser.NoSectionError
   ConfigParser.NoOptionError

ConfigParser
------------

These are the `ConfigParser` methods that will be used.

.. currentmodule:: ConfigParser
.. autosummary::
   :toctree: api

   SafeConfigParser
   SafeConfigParser.options
   SafeConfigParser.read
   SafeConfigParser.get
   SafeConfigParser.getint
   SafeConfigParser.getfloat
   SafeConfigParser.getboolean
   SafeConfigParser.items
