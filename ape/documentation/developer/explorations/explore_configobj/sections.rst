Sections
========

`ConfigObj` objects are sub-classes of the `Section` class (which is itself a sub-class of the `dict`). Besides the dictionary methods that Section inherits, it also contributes some of its own. I'm not planning to use most of them so I'll just look at the type-casting and `merge` methods here.



Type Casting
------------

.. module:: configobj
.. autosummary::
   :toctree: api

   Section
   Section.as_bool
   Section.as_int
   Section.as_float
   Section.as_list

The type-casting methods for the `Section` behave pretty much like the `ConfigParser` `get` methods except with the addition of a list option.

::

    text = """
    [test]
    ape = grape
    turned = on
    count = 10
    weight = 32.3
    tarts = apple, rhubarb
    """
    



Since ConfigObj will break the list up ('tarts') when the object is created I'll set `list_values` to False in the constructor.

.. '

::

    parser = SafeConfigParser()
    parser.readfp(StringIO(text))
    
    config = ConfigObj(text.splitlines(), list_values=False)
    



First ConfigParser.

::

    print 'ape: ', parser.get('test', 'ape')
    print 'turned: ', parser.getboolean('test', 'turned')
    print 'count: ', parser.getint('test', 'count')
    print 'weight: ', parser.getfloat('test', 'weight')
    try:
        print 'tarts: ', parser.getlist('test', 'tarts')
    except AttributeError as error:
        print error
    
    

::

    ape:  grape
    turned:  True
    count:  10
    weight:  32.3
    tarts:  SafeConfigParser instance has no attribute 'getlist'
    
    



Now ConfigObj.

::

    section = config['test']
    print 'ape: ', section['ape']
    print 'turned: ', section.as_bool('turned')
    print 'count: ', section.as_int('count')
    print 'weight: ', section.as_float('weight')
    print 'tarts: ', section.as_list('tarts')
    
    

::

    ape:  grape
    turned:  True
    count:  10
    weight:  32.3
    tarts:  ['apple, rhubarb']
    
    



The `as_list` method doesn't work the way I thought it would, all it did was put the string into a list, it didn't split the value into a comma-separated list. I'm not really sure why this is useful.

.. '

Merge
-----

.. autosummary::
   :toctree: api

   Section.merge

An interesting method is the `merge` method. It updates an existing Section with values from another, allowing you to create a default ConfigObj and replace only the values that the user set.

::

    update_text = """
    [test]
    tarts = Sally, Jessie, Rhubarb
    """.splitlines()
    
    update_config = ConfigObj(update_text)
    config.merge(update_config)
    
    section = config['test']
    
    for key, value in section.iteritems():
        print "{0}: {1}".format(key, value)
    
    

::

    ape: grape
    turned: on
    count: 10
    weight: 32.3
    tarts: ['Sally', 'Jessie', 'Rhubarb']
    
    



Merging Sub-Sections
--------------------

::

    default = """
    [ape]
    cow = boy
     [[chimp]]
     boy = howdy
    """.splitlines()
    config = ConfigObj(default)
    
    update = """
    cow = man
    boy = girl
    """.splitlines()
    
    update_config = ConfigObj(update)
    
    config.merge(update_config)
    
    for key, value in config.iteritems():
        print "{0}: {1}".format(key, value)
    
    

::

    cow: man
    boy: girl
    ape: {'cow': 'boy', 'chimp': {'boy': 'howdy'}}
    
    



Well, that didn't work. It looks like ConfigObj respects nesting when updating (which seems a good thing) so it added the key-value pairs to the root section.

.. '

::

    # first get rid of the mistake
    del(config['cow'])
    del(config['boy'])
    
    update = """
    [[chimp]]
    boy = girl
    """.splitlines()
    
    try:
        update_config = ConfigObj(update)
    except NestingError as error:
        print error
    
    

::

    Section too nested at line 2.
    
    



Oops. Even though we're changing only the value in the 'chimp' section we have to create the tree-structure for ConfigObj (once again this seems a good thing).

.. '

::

    update = """
    [ape]
    [[chimp]]
    boy = girl
    """.splitlines()
    
    update_config = ConfigObj(update)
    
    config.merge(update_config)
    
    for key, value in config.iteritems():
        print "{0} {1}".format(key, value)
    
    

::

    ape {'cow': 'boy', 'chimp': {'boy': 'girl'}}
    
    



There are other methods as well, but I can't see a use for them right now. Even the type-casting seem superfluous, especiall if you're using schema-validation, but I thought they'd be interesting to see.
