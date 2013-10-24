Exploring External Imports
==========================

.. _exploring-external-imports:

The goal is to be able to import plugins that have been created in external packages so that there won't be a need to put everything into the `ape`. This is an exploration of how that might work.

.. superfluous '

::

    # python standard library
    import importlib
    import inspect
    
    # ape
    from ape.plugins.base_plugin import BasePlugin
    



Testing An Import
-----------------

There is a folder structure below this one that looks like::

    fake_package/
        setup.py
        fakepackage/
            __init__.py
            fakeplugin.py

Since there's no ``__init__.py`` in the `fake_package` folder, it should not be picked up as part of this package. The goal is to import the :ref:`FakePlugin <fake-plugin>` from this package.

.. the reference to fake-plugin won't get picked up since it's in another package
.. superfluous '            
    
::

    module_name = 'fakepackage.fakeplugin'
    module = importlib.import_module(module_name)
    members = inspect.getmembers(module,
                                 lambda o: inspect.isclass(o) and
                                 o.__base__ is BasePlugin)
    for member in members:
        name, definition = member
        print name
        d = definition()
        d.fetch_config()
    

::

    FakePlugin
    
    [FAKEPLUGIN]
    #this is a fake plugin that creates a DummyClass instance
    # anything put in this section will be logged
    # but nothing will be done with it
    
    

