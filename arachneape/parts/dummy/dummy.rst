The Dummy
=========


The Dummy Class
---------------

.. currentmodule:: arachneape.components.dummy.dummy
.. _dummy-class:
The Dummy module holds dummy classes that do nothing. They is primarily used to test implementations of infrastructure components.

.. uml::

   DummyClass -|> BaseClass
   DummyClass o- CallClass

.. currentmodule:: arachneape.parts.dummy.dummy   
.. autosummary::
   :toctree: api

   DummyClass

The Dummy Class logs (at the `info`) level when it is created and when it is called.



A Crash Dummy
-------------

This is a Dummy that raises an error when called.






An Example
----------

As an example we can create an operator and make some fake calls to it (I do not think the logging will get captured by Pweave, though).

::

    if output_documentation:
        class FakeLogger(object):
            def info(self, output):
                print output
                
        class KingKong(DummyClass):
            def __init__(self, *args, **kwargs):
                super(KingKong, self).__init__(*args, **kwargs)
                self._logger = FakeLogger()
                return
        
    
        kongs = (KingKong(index, name) for index,name in enumerate('Kong MightyJoe'.split()))
        for kong in kongs:
            kong.rampage()
            kong('fay wray')
    

::

    '[34mrampage[0;0m' attribute called on [31mKingKong[0;0m
    [31mKingKong[0;0m Called
    [1mArgs:[0;0m ('fay wray',)
    [1mKwargs:[0;0m {}
    '[34mrampage[0;0m' attribute called on [31mKingKong[0;0m
    [31mKingKong[0;0m Called
    [1mArgs:[0;0m ('fay wray',)
    [1mKwargs:[0;0m {}
    



I had to add a fake logger because pweave does not capture logging output. If you run this module::

    python dummy.py

You should see what is being sent to the logger in full color (without the extra ANSI codes).

