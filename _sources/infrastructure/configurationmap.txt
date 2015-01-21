The Configuration Map
=====================

.. _configuration-map:

The `Configuration Map` maps a configuration-file-name to data. It extends `ConfigObj` to have more data-types.

.. _configurationmap-background:    
    
Background
----------

The `ConfigObj` module will be used to find and convert files to data. ConfigObj has methods for the main singular data-types but I will also add collections and times. 






.. _configurationmap-uml:

UML Model
---------

.. uml::

   ConfigurationMap -|> BaseClass
   ConfigurationMap o- ConfigParser

.. _configurationmap-configurationerror:   

The ConfigurationError
----------------------

The `ConfigurationMap` will raise a ConfigurationError to try and trickle up more useful information.

.. module:: theape.infrastructure.errors
.. autosummary::
   :toctree: api

   ConfigurationError




.. _configurationmap-api:

The API
-------

.. module:: theape.infrastructure.configurationmap
.. autosummary::
   :toctree: api

   ConfigurationMap
   ConfigurationMap.get
   ConfigurationMap.get_type
   ConfigurationMap.get_int
   ConfigurationMap.get_float
   ConfigurationMap.get_boolean
   ConfigurationMap.get_relativetime
   ConfigurationMap.get_datetime
   ConfigurationMap.get_list
   ConfigurationMap.get_dictionary
   ConfigurationMap.get_ordered_dictionary
   ConfigurationMap.get_named_tuple
   ConfigurationMap.sections
   ConfigurationMap.has_option
   ConfigurationMap.options
   ConfigurationMap.items
   ConfigurationMap.defaults
   ConfigurationMap.write

.. note:: get_relativetime and get_absolutetime are currently using the defaults. If more control is needed, you will need to grab the option and build them yourself.
   
.. _configurationmap-parser:   

The ConfigurationMap.parser
---------------------------

This property is a SafeConfigParser instance. When it is created, the ConfigurationMap reads the filename passed in on instantiation and checks if the loaded configuration has a ``[DEFAULT] : config_glob`` option. If it does, it gets the `config_glob` value, traverses the expanded glob and loads all the files that match.

.. _configurationmap-configparser:

ConfigParser
------------

These are the `ConfigParser` methods that will be used.

.. currentmodule:: ConfigParser
.. autosummary::
   :toctree: api

   SafeConfigParser
   SafeConfigParser.options
   SafeConfigParser.sections
   SafeConfigParser.items
   SafeConfigParser.read
   SafeConfigParser.write
   SafeConfigParser.get
   SafeConfigParser.getint
   SafeConfigParser.getfloat
   SafeConfigParser.getboolean
   SafeConfigParser.has_option
   SafeConfigParser.has_section

.. _configurationmap-exceptions:
   
ConfigParser Exceptions
-----------------------

These are the `ConfigParser` Exceptions that I will handle in the `ConfigurationMap`.

.. currentmodule:: ConfigParser
.. autosummary::
   :toctree: api

   ConfigParser.Error
   ConfigParser.NoSectionError
   ConfigParser.NoOptionError

.. _configurationmap-module-diagram:
   
Module Diagram
--------------


[Errno 2] No such file or directory
Is pylint installed?
.. image:: classes_configurationmap.png



.. .. _configurationmap-class-implementation-diagram:
.. 
.. Class Implementation Diagram
.. ----------------------------
.. 
.. <<name='class_diagram', echo=False, results='sphinx'>>=
.. if IN_PWEAVE:
..     class_diagram_file = class_diagram(class_name="ConfigurationMap",
..                                        filter='OTHER',
..                                        module=this_file)
..     print ".. image:: {0}".format(class_diagram_file)
.. @
