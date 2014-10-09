Basic ConfigObj
===============

Here we'll look at using ConfigObj to parse a user's configuration file.

::

    # python standard library
    from StringIO import StringIO
    
    # third party
    from configobj import ConfigObj
    



The ConfigObj object inherits from the configobj.Section class which itself extends python's `dict`.

.. uml::

   dict <|-- Section
   Section <|-- ConfigObj

So most retrievals will look like you're using a dictionary of dictionaries.

Root Options
------------

Unlike python's ConfigParser, ConfigObj lets you put values in the configuration with no section header.

::

    sample = ["name = John Bigboote"]
    
    config = ConfigObj(sample)
    print config['name']
    
    

::

    John Bigboote
    
    



ConfigObj also supports comma-separated lists by default.

::

    sample = ["diseases = ebola, syphillis, cooties"]
    config = ConfigObj(sample)
    print config['diseases']
    
    

::

    ['ebola', 'syphillis', 'cooties']
    
    



What if your value has a comma?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    sample = ["quote = What's this, then?"]
    config = ConfigObj(sample)
    print config['quote']
    
    

::

    ["What's this", 'then?']
    
    



In this case you can set the `list_values` parameter to False

::

    config = ConfigObj(sample, list_values=False)
    print config['quote']
    
    

::

    What's this, then?
    
    



.. note:: This parameter has to be set in the constructor, changing the objects 'list_values' attribute won't work.

::

    config = ConfigObj(sample)
    config.list_values = False
    print config['quote']
    
    

::

    ["What's this", 'then?']
    
    



This makes it difficult to have cases where you have lists and non-lists in the same configuration. It's probably better to let the validation take care of converting values to non-strings.


Sections and Sub-Sections
-------------------------

ConfigObj handles sections much like ConfigParser so can be used where the configuration follows the ini-format.

::

    sample = StringIO("""
    default = this
    [grape]
    name = ape
    value = 1
    """)
    
    config = ConfigObj(sample)
    print config
    
    

::

    {'default': 'this', 'grape': {'name': 'ape', 'value': '1'}}
    
    



Looking at the output you can see that adding sections adds an inner dictionary. To access the values you still use the dict interface.

::

    print config['default']
    print config['grape']['name']
    print config['grape']['value']
    
    

::

    this
    ape
    1
    
    



To add more structure to the configuration you can also add sub-sections by adding more brackets around the headers.

::

    sample = StringIO("""
    [top]
    top_value = 0
      [[level1]]
      level1_value = 1
    
        [[[level2]]]
        level2_value = 2
    
    [topcow]
    topcow_value = moo
    """)
    config = ConfigObj(sample)
    
    print "Top Value: ", config['top']['top_value']
    print "Level1 Value", config['top']['level1']['level1_value']
    
    print "Level2 Value", config['top']['level1']['level2']['level2_value']
    
    print "Top Cow: ", config['topcow']['topcow_value']
    
    
    

::

    Top Value:  0
    Level1 Value 1
    Level2 Value 2
    Top Cow:  moo
    
    

