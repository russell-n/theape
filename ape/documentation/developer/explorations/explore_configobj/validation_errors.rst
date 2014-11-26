Validation Errors
=================

This is an exploration of the `flatten_errors` function given to check validation errors.

::

    from configobj import ConfigObj, flatten_errors
    from validate import Validator
    
    



Literal String
--------------

One of the things that I want to check is to see if the plugin was given the correct configuration.

::

    configspec="""
    [TEST]
    value = LiteralString
    """.splitlines()
    
    config = """
    [TEST]
    value = NonLiteralString
    """.splitlines()
    
    config_spec = ConfigObj(configspec,
                            list_values=False,
                            _inspec=True)
    configuration = ConfigObj(config, configspec=configspec)
    
    validator = Validator()
    
    outcome = configuration.validate(validator, preserve_errors=True)
    print outcome
    

::

    {'TEST': {'value': VdtUnknownCheckError('the check "LiteralString" is unknown.',)}}
    



So, it appears that you can't just make up names in the configspec. What if we give it a single option?
.. '

::

    configspec="""
    [TEST]
    value = option('LiteralString')
    """.splitlines()
    
    config_spec = ConfigObj(configspec,
                            list_values=False,
                            _inspec=True)
    
    configuration = ConfigObj(config, configspec=configspec)
    outcome = configuration.validate(validator, preserve_errors=True)
    print outcome
    

::

    {'TEST': {'value': VdtValueError('the value "NonLiteralString" is unacceptable.',)}}
    



This seems to be what we want. But now how do you use `flatten_errors`? First, let's see what `outcome` is when the value is correct.
.. '

::

    config = """
    [TEST]
    value = LiteralString
    """.splitlines()
    
    configuration = ConfigObj(config,
                              configspec=configspec)
    outcome = configuration.validate(validator, preserve_errors=True)
    print outcome
    

::

    True
    



So, instead of a dictionary it returns `True`. Now let's try and flatten the errors.
.. '

::

    def process_errors(config, outcome):
        """
        Uses `flatten_errors` to find bad values
    
        :param:
    
          - `config`: ConfigObj that created the outcome
          - `outcome`: returned value from config.validate
        """
        if outcome:
            for section_list, key, error in flatten_errors(config, outcome):
                if key is not None:
                    print "The '{0}' key in section '{1}' failed validation (error='{2}')".format(key,
                                                                                    ','.join(section_list),
                                                                                    error)
                else:
                    print "The '{0}' section was missing".format(','.join(section_list))
        return
        
    

::

    config = """
    [TEST]
    value = BadValue
    """.splitlines()
    
    configuration = ConfigObj(config,
                              configspec=configspec)
    outcome = configuration.validate(validator, preserve_errors=True)
    process_errors(configuration, outcome)
    

::

    The 'value' key in section 'TEST' failed validation (error='the value "BadValue" is unacceptable.')
    



Missing Value
-------------

Okay, so that was the bad-value. What about a missing value?

::

    config_spec = """
    [TEST]
    option_1 = option('LiteralStringValue')
    option_2 = integer
    """.splitlines()
    configspec = ConfigObj(config_spec,
                           list_values=False,
                           _inspec=True)
    



Now the configuration.

::

    config = """
    [TEST]
    option_1 = LiteralStringValue
    """.splitlines()
    
    configuration = ConfigObj(config, configspec=configspec)
    outcome = configuration.validate(validator, preserve_errors=True)
    process_errors(configuration, outcome)
    

::

    The 'option_2' key in section 'TEST' failed validation (error='False')
    



That didn't work the way I thought it would. It looks like setting `preserve_errors` changes the behavior... I need to change `process_errors`.
.. '

Process Errors 2
~~~~~~~~~~~~~~~~

::

    def process_errors_2(config, outcome):
        """
        Uses `flatten_errors` to find bad values
    
        :param:
    
          - `config`: ConfigObj that created the outcome
          - `outcome`: returned value from config.validate
        """
        if outcome:
            for sections, option, error in flatten_errors(config, outcome):
                section = ','.join(sections)
                if option is not None:
    
                    if error:
                        print "Option '{0}' in section '{1}' failed validation (error='{2}')".format(option,
                                                                                                    section,
                                                                                                    error)
                    else:
                        print "Option '{0}' in section '{1}' was missing.".format(option,
                                                                                    section)
                else:
                    print "The '{0}' section was missing".format(section)
        return
        
    



Now check again.

::

    outcome = configuration.validate(validator, preserve_errors=True)
    process_errors_2(configuration, outcome)
    

::

    Option 'option_2' in section 'TEST' was missing.
    



All Bad Values
--------------

Now that we have a working `process_errors_2` function, let's see what happens if both the values are bad.
.. '

::

    config = """
    [TEST]
    option_1 = BadValue
    option_2 = apple
    """.splitlines()
    
    configuration = ConfigObj(config,
                              configspec=configspec)
    outcome = configuration.validate(validator, preserve_errors=True)
    process_errors_2(configuration, outcome)
    

::

    Option 'option_1' in section 'TEST' failed validation (error='the value "BadValue" is unacceptable.')
    Option 'option_2' in section 'TEST' failed validation (error='the value "apple" is of the wrong type.')
    



Missing Section
---------------

Just for completeness, we'll make sure that the `process_errors_2` function handles missing sections correctly.
.. '

::

    config_spec = """
    [TEST]
    option_1 = integer
    
    [[SUBTEST]]
    option_2 = float
    """.splitlines()
    
    configspec = ConfigObj(config_spec,
                           list_values=False,
                           _inspec=True)
    config = """
    [TEST]
    option_1 = 1
    option_2 = 2
    """.splitlines()
    
    configuration = ConfigObj(config,
                              configspec=configspec)
    outcome = configuration.validate(validator, preserve_errors=True)
    process_errors_2(configuration, outcome)
    

::

    The 'TEST,SUBTEST' section was missing
    



The output isn't as intuitive as I would like, but I'm not sure it's worth the effort to build up the brackets.
.. '

Extras
------

Just to be safe, I'll check to make sure that extra options don't create errors.

::

    config = """
    [TEST]
    option_1 = 2
    
    [[SUBTEST]]
    option_2 = 3.5
    option_4 = 5
    """.splitlines()
    configuration = ConfigObj(config,
                              configspec=configspec)
    outcome = configuration.validate(validator, preserve_errors=True)
    process_errors_2(configuration, outcome)
    
    

