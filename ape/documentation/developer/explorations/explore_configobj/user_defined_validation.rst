User Defined Validation
=======================



A More Complete Settings Section
--------------------------------

One of the things that differs about the 'SETTINGS' section in the `ape` is that I'm using ape-classes to create the time-objects (`total_time` and `end_time`).

.. '

::

    settings_config = """
    [SETTINGS]
    repetitions = 11
    total_time = 3 days 2 Hours 12 minutes
    end_time = 8:00 pm
    external_modules = tuna.annealing
    subfolder = output
    timestamp = HH:MM
    """.splitlines()
    



The original APE used the configuration map to get them.

.. module:: ape.infrastructure.configurationmap
.. autosummary::
   :toctree: api

   ConfigurationMap.get_relativetime
   ConfigurationMap.get_datetime

.. module:: ape.infrastructure.timemap
.. autosummary::
   :toctree: api

   RelativeTime
   AbsoluteTime

This means we have to tell the validator to use these classes.

::

    section_spec = """
    [SETTINGS]
    repetitions = integer(min=0, default=1)
    total_time = relative_time(default=None)
    end_time = absolute_time(default=None)
    external_modules = string(default=None)
    subfolder = string(default=None)
    timestamp = string(default=YY:HH:MM:SS)
    """.splitlines()
    
    settings_configspec = ConfigObj(section_spec,
                                    list_values=False,
                                    _inspec=True)
    



Now we add the constructors to the validator. The key-names have to match what's in the spec and the values have to be the actual function definitions (in this case the class definitions). This could also be set by passing in a dictionary when the Validator was created.

.. '

::

    validator = Validator()
    validator.functions['relative_time'] = RelativeTime
    validator.functions['absolute_time'] = AbsoluteTime()
    



Now we try and validate the configuration.

::

    config = ConfigObj(settings_config,
                       configspec=settings_configspec)
    config.validate(validator)
    



Now the output.

::

    for option, value in config['SETTINGS'].iteritems():
        print "Option: '{0}', Value: '{1}', Type: '{2}'".format(option, value,
                                                                type(value))
    

::

    Option: 'repetitions', Value: '11', Type: '<type 'int'>'
    Option: 'total_time', Value: '3 days 2 Hours 12 minutes', Type: '<class 'ape.infrastructure.timemap.RelativeTime'>'
    Option: 'end_time', Value: '2014-11-17 20:00:00', Type: '<type 'datetime.datetime'>'
    Option: 'external_modules', Value: 'tuna.annealing', Type: '<type 'str'>'
    Option: 'subfolder', Value: 'output', Type: '<type 'str'>'
    Option: 'timestamp', Value: 'HH:MM', Type: '<type 'str'>'
    

