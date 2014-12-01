Extra Values
============

When you validate a configuration `configobj` can tell you which options or sections in the configuration weren't in your `configspec` this can be useful for finding errors in the user's configuration when specifying optional values (presumably option-name misspellings).

Getting Extra Values
--------------------

::

    config_spec = """
    [TEST]
    option_1 = integer
    
    [[SUBTEST]]
    option_2 = integer
    """.splitlines()
    
    configspec = ConfigObj(config_spec,
                           list_values=False,
                           _inspec=True)
    
    config = """
    extra = option
    
    [TEST]
    option_1 = 1
    option_3 = 3
    
    [[SUBTEST]]
    option_2 = 2
    option_4 = 4
    
    [[SUBTEST2]]
    option_5 = 5
    
    [[[SUBSUBTEST]]]
    option_6 = 6
    """.splitlines()
    
    configuration = ConfigObj(config,
                              configspec=configspec)
    validator = Validator()
    
    outcome = configuration.validate(validator)
    assert outcome
    



Now the extra values.

::

    for sections, option in  get_extra_values(configuration):
        print sections, option
    

::

    () extra
    ('TEST',) option_3
    ('TEST',) SUBTEST2
    ('TEST', 'SUBTEST') option_4
    



According to the documentation, the return value for `get_extra_values` is a list of tuples. looking at the output it appears they are of the form `((section, subsection), option)`, with the subsection being empty for the top-section. The sub-sections also appear to only go one deep so it isn't a tree going all the way to the leaves.
.. '

Getting the Values
------------------

This is the way the documentation suggests getting the values.

::

    def process_extras(configuration, verbose=True):
        had_extras = False
    
        for sections, name in get_extra_values(configuration):
            had_extras = True
            bottom_section = configuration
            for section in sections:
                bottom_section = bottom_section[section]
            value = bottom_section[name]
            item_type = 'Value'
            if isinstance(value, dict):
                item_type = 'Section'
            section = ','.join(sections) or 'top level'
            if verbose:
                message = "Extra entry in '{0}' section. {1}: '{2}'".format(section,
                                                                    item_type,
                                                                    name)
                if item_type == 'Value':
                    message += '= {0}'.format(value)
                print message
        return had_extras
    

::

    process_extras(configuration)
    

::

    Extra entry in 'top level' section. Value: 'extra'= option
    Extra entry in 'TEST' section. Value: 'option_3'= 3
    Extra entry in 'TEST' section. Section: 'SUBTEST2'
    Extra entry in 'TEST,SUBTEST' section. Value: 'option_4'= 4
    



No Missing Values
-----------------

While printing this information is useful, I think it would be useful to check if there actually were extra values. What happens when the configuration doesn't have extra values?
..'
    
::

    config_2 = """
    [TEST]
    option_1 = 2
    
    [[SUBTEST]]
    option_2 = 1
    """.splitlines()
    

::

    configuration_2 = ConfigObj(config_2,
                                configspec=configspec)
    had_extras = process_extras(configuration_2, False)
    print "There were extras in the second configuration: {0}".format(had_extras)
    print "There were extras in the first configuration: {0}".format(process_extras(configuration, False))
    

::

    There were extras in the second configuration: False
    There were extras in the first configuration: True
    



So it looks like all you have to do is see if get extra_values puts anything in the returned list.

::

    extra_1 = get_extra_values(configuration)
    extra_2 = get_extra_values(configuration_2)
    
    print extra_1
    print len(extra_1)
    print extra_2
    print len(extra_2)
    

::

    [((), 'extra'), (('TEST',), 'option_3'), (('TEST',), 'SUBTEST2'), (('TEST', 'SUBTEST'), 'option_4')]
    4
    []
    0
    

