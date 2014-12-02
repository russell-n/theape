Merging Sections
================

The main reason for using ConfigObj is to enable sub-tree configurations under the `PLUGINS` section. My initial assumption that I could use ``configspec`` to filter out the other plugins was wrong (otherwise the ``check_extra_values`` function would not make as much sense) so I'm going to try and work it out here.
.. '



The Configspecs
---------------

I'm going to assume that there is only one type of plugin and that both of them are the same plugin type. Rather than re-type the second plugin configuration completely, I'll see if we can use ``merge`` to take the first plugin and update it with the second.

::

    plugin_configspec = """
    plugin = string
    updates_section = string(default=None)
    
    [sub_section]
    op1 = integer
    op2 = integer
    """.splitlines()
    



The configspec doesn't have the section name defined so that it can be used by multiple plugin sections. Now the test configuration.
.. '

The Configuration
-----------------

::

    plugin_configuration = """
    [PLUGINS]
    
    [[FAKE]]
    plugin = Fake
    
    [[[sub_section]]]
    op1 = 1
    op2 = 2
    
    [[FAKE2]]
    updates_section = FAKE
    
    [[[sub_section]]]
    op2 = 3
    """.splitlines()
    



First, the Operator is going to get the plugins section.

::

    sections = ConfigObj(plugin_configuration)
    plugin_sections  = ConfigObj(sections['PLUGINS'])
    print plugin_sections
    

::

    {'FAKE': {'plugin': 'Fake', 'sub_section': {'op1': '1', 'op2': '2'}}, 'FAKE2': {'updates_section': 'FAKE', 'sub_section': {'op2': '3'}}}
    



That was pretty straight-forward, but I figured I might as well check and make sure it behaves like I thought it does. One thing to note is that if the code that gets the 'PLUGINS' section requires that each section has a `plugin` defined then even the section that is being updated will need it. It might make more sense to require either the `plugin` or the `updates_section` but not both. Or don't require either and raise an error if they are both missing. That might be the best option, especially since both of those opitons are just strings. That's not what this is about, though, so we'll just assume that it's being checked elsewhere.

The FAKE Section
----------------

The first order is to get the first ('FAKE') section.

::

    fake_section = ConfigObj(plugin_sections['FAKE'],
                             configspec=plugin_configspec)
    
    validator = Validator()
    print fake_section.validate(validator)
    

::

    True
    



.. csv-table:: Fake Section
   :header: Section,Option, Type, Value
   :delim: ;
   
   Top;plugin;<type 'str'>;Fake
   Top;updates_section;<type 'NoneType'>;None
   Top;sub_section;<class 'configobj.Section'>;{'op1': 1, 'op2': 2}
   sub_section;op1;<type 'int'>;1
   sub_section;op2;<type 'int'>;2



From the output we can see that this has a plugin name ('Fake'), no 'updates_section' option, and both options have been cast to integers as expected.

Fake 2
------

Now comes the part that we're really interested in, building the 'FAKE2' section using the 'FAKE' section.
.. '

::

    update_section = ConfigObj(plugin_sections['FAKE2'],
                               configspec=plugin_configspec)
    
    other_section = update_section['updates_section']
    
    if other_section is not None:
        fake_2_section_source = ConfigObj(plugin_sections[other_section],
                                configspec=plugin_configspec)
        fake_2_section_source.merge(update_section)
        update_section = fake_2_section_source
    
    print update_section.validate(validator)
    

::

    True
    



.. csv-table:: Fake2 Section
   :header: Section,Option, Type, Value
   :delim: ;
   
   Top;plugin;<type 'str'>;Fake
   Top;updates_section;<type 'str'>;FAKE
   Top;sub_section;<class 'configobj.Section'>;{'op1': 1, 'op2': 3}
   sub_section;op1;<type 'int'>;1
   sub_section;op2;<type 'int'>;3



So now the second section has the 'FAKE' values but 'updates_section' is True and 'op2' has been changed to 3. I think this pattern will work. The conditional that checks if ``other_section`` wasn't needed since we're creating it specifically to have this option, but I think something like that is how it will be used so I put it there in case I forget later on. One thing to remember is that the sub-section level is being greatly reduced (triple-brackets for the 'sub_section' in the original configuration, but single-brackets in the `configspec`) so this can get confusing. Sub-sections should probably be avoided if possible.

An Alternative Scheme
---------------------

My original idea was that the configspec should be a string with string formatting to set the section name.

::

    plugin_configspec_2 = """
    [{section}]
    plugin = string
    updates_section = string(default=None)
    
    [[sub_section]]
    op1 = integer
    op2 = integer
    """
    



Alternate Fake Section
~~~~~~~~~~~~~~~~~~~~~~

So to use the new plugin configspec you need to change it first.

::

    f_spec = plugin_configspec_2.format(section='FAKE').splitlines()
    f_section = ConfigObj(plugin_sections,
                          configspec=f_spec)
    print f_section
    

::

    {'FAKE': {'plugin': 'Fake', 'sub_section': {'op1': 1, 'op2': 3}}, 'FAKE2': {'updates_section': 'FAKE', 'sub_section': {'op2': '3'}}}
    



So, two observations. One is that both sections are there in the section (the 'FAKE2' section will show up in an extra-values check) and the options in the section have already been converted, even though I didn't validate. It looks like maybe there's some kind of side-effect going on. Tray that again.

::

    sections = ConfigObj(plugin_configuration)
    plugin_sections_2  = ConfigObj(sections['PLUGINS'])
    
    f_section = ConfigObj(plugin_sections_2,
                          configspec=f_spec)
    print f_section
    

::

    {'FAKE': {'plugin': 'Fake', 'sub_section': {'op1': '1', 'op2': '2'}}, 'FAKE2': {'updates_section': 'FAKE', 'sub_section': {'op2': '3'}}}
    



That's more like it. *Now* try the validation.
.. '

::

    print f_section.validate(validator)
    print f_section['FAKE']
    

::

    True
    {'plugin': 'Fake', 'updates_section': None, 'sub_section': {'op1': 1, 'op2': 2}}
    




Alternate Fake2 Section
~~~~~~~~~~~~~~~~~~~~~~~

So, now we can try the same thing with the second section.

::

    section_name = 'FAKE2'
    f2_spec = plugin_configspec_2.format(section=section_name).splitlines()
    
    sections = ConfigObj(plugin_configuration)
    plugin_sections_2  = ConfigObj(sections['PLUGINS'])
    
    f_2_section = ConfigObj(plugin_sections_2)
    
    update_section_2 = f_2_section[section_name]
    
    if update_section_2['updates_section'] is not None:
        other_section = update_section_2['updates_section']
    
        # note the configspec
        source_section = ConfigObj(f_2_section[other_section],
                                   configspec=f2_spec)
        source_section.merge(update_section_2)
        update_section_2 = source_section
    
    print update_section_2.validate(validator)
    print update_section_2
    

::

    False
    {'plugin': 'Fake', 'updates_section': 'FAKE', 'sub_section': {'op1': '1', 'op2': '3'}, 'FAKE2': {'updates_section': None, 'sub_section': {}}}
    



You'll note that this really doesn't work. To merge the two you have to separate the sections, but once you do this the section names are lost so the configspec has to be the original one without the section-name in it. Time to abandon this idea.
