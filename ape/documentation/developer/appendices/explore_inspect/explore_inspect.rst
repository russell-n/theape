Python Inspect
==============

This is an exploration of the python `inspect <http://docs.python.org/2/library/inspect.html>`_ module. I have come to the conclusion that the `yapsy <http://yapsy.sourceforge.net/>`_ system, while interesting in its own right, is too confusing and big to make sense for the limited things that I want to do with it so this is an attempt to get to know ``inspect`` in the hopes that it has enough for me to use.

To start I will use a :ref:`dummy module <inspect-dummy-module>` and see what I can get from it. 

::

    # python standard library
    import inspect
    
    # this package
    import dummy
    
    



The Docstring
-------------

The ``inspect.getdoc`` gets document strings for objects and formats them.

First the module docstring:

::

    print inspect.getdoc(dummy)
    

::

    None
    



Now a class inside the module:

::

    print inspect.getdoc(dummy.DummyClass)
    

::

    This is a dummy class that inherits from `object`
    



What about a method for the class?

::

    print inspect.getdoc(dummy.DummyClass.a_tuple)
    

::

    Puts self.a in a tuple and returns it
    
    :return: (self.a, )
    



I was actually execting that to fail since I used the class definition instead of an instance, but I guess it works.

Get File
--------

The ``inspect.getfile`` method takes an object and tells you the file where it came from:

::

    from dummy import DummyClass
    d = DummyClass(a=1)
    print inspect.getfile(DummyClass)
    
    try:
        print inspect.getfile(d)
    except TypeError as error:
        print error
    

::

    ./dummy.py
    <dummy.DummyClass object at 0x353da10> is not a module, class, method, function, traceback, frame, or code object
    



So, I apparently misunderstood the meaning of the word `object`, it appears to mean the definition, not an instance of the class I defined.

getargspec
----------

``inspect.getargspec`` should tell you what the arguments are for a method (I think).

::

    print inspect.getargspec(DummyClass.convoluted)
    

::

    ArgSpec(args=['self', 'a', 'b', 'c', 'd'], varargs=None, keywords=None, defaults=(5, '9', None))
    



That does not appear to be as useful as I thought it would be.

getmembers
----------

``inspect.getmembers`` returns members of an object, allowing you to pass in a function to filter the particular members you want.

::

    print inspect.getmembers(dummy, inspect.isclass)
    

::

    [('ABCMeta', <class 'abc.ABCMeta'>), ('AnotherClass', <class 'dummy.AnotherClass'>), ('ConcretePlugin', <class 'dummy.ConcretePlugin'>), ('DummyClass', <class 'dummy.DummyClass'>), ('PluginBase', <class 'dummy.PluginBase'>), ('abstractproperty', <class 'abc.abstractproperty'>)]
    



I was thinking I could do something like:

::

    print inspect.getmembers(dummy, lambda o: inspect.isclass(o) and o.__name__.startswith('Dummy'))
    

::

    [('DummyClass', <class 'dummy.DummyClass'>)]
    



Or maybe (if the classes I want have to be children of the same class):

::

    print inspect.getmembers(dummy, lambda o: inspect.isclass(o) and o.__base__ is DummyClass)
    

::

    [('AnotherClass', <class 'dummy.AnotherClass'>)]
    



I had thought that I would be matching the name of the base-class but __base__ returns a type object.

Discovering Modules
-------------------

One of the things that maybe can be done is import modules on the fly. Here I will look for:

.. currentmodule:: arachneape.documentation.developer.appendices.explore_inspect.dummy

.. autosummary::
   :toctree: api

   ConcretePlugin

::

    import os
    import importlib
    
    from dummy import PluginBase
    
    for filename in os.listdir(os.getcwd()):
        # the print statements in this module are showing up in the output when I import it
        if filename.endswith('.py') and not filename=='explore_inspect.py':
            base, extension = os.path.splitext(filename)
            try:
                candidate = importlib.import_module(base)
            except ImportError as error:
                # for some reason nose is using /usr/lib/python2.7/importlib
                # and this is causing it to fail
                print error
                continue        
            members = inspect.getmembers(candidate, lambda o: inspect.isclass(o) and o.__base__ is PluginBase)
            for member in members:
                name, definition = member
                print name
                m = definition()
                print 'Help:'
                print m.help_string
                print "Config:"
                print m.config
                print "Product:"
                print m.product
    

::

    No module named arachneape.commoncode.index_builder
    ConcretePlugin
    Help:
    
            Now is the winter of our disconcent.
            
    Config:
    
            [CONCRETE]
            zero = 0
            
    Product:
    0
    



Presumably in the real code there would be some variation of ``__package__`` in there instead of current-working-directory, but in Pweave it returns None for some reason.





