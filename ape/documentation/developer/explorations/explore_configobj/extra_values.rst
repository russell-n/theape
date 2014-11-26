Extra Values
============

When you validate a configuration `configobj` can tell you which options or sections in the configuration weren't in your `configspec` this can be useful for finding errors in the user's configuration when specifying optional values (presumably option-name misspellings).

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

    def process_extras(configuration):
        for sections, name in get_extra_values(configuration):
            bottom_section = configuration
            for section in sections:
                bottom_section = bottom_section[section]
            value = bottom_section[name]
            item_type = 'Value'
            if isinstance(value, dict):
                item_type = 'Section'
            section = ','.join(sections) or 'top level'
            print "Extra entry in '{0}' section. {1}: '{2}'".format(section,
                                                                    item_type,
                                                                    name)
        return
    

::

    process_extras(configuration)
    

::

    Extra entry in 'top level' section. Value: 'extra'
    Extra entry in 'TEST' section. Value: 'option_3'
    Extra entry in 'TEST' section. Section: 'SUBTEST2'
    Extra entry in 'TEST,SUBTEST' section. Value: 'option_4'
    

