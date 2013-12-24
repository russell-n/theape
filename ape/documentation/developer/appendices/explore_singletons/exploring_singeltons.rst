Exploring Singletons
====================

.. _ape-documentation-exploring-singletons:

Introduction
------------

This won't be an extensive exploration since it seems to be relatively straightforward. This is a test of creating a `singleton <http://en.wikipedia.org/wiki/Singleton_pattern>`_ in python. The motivation for it is that I want to allow plugins to add themselves to aggregating composites without having to worry if others have alread created one. 

The Idea
--------

To create the singleton you just need to rely on the fact that when you make multiple calls to the same module in python, the interpreter only creates one instance of it. So you can create a function in it that instantiates the object and even if multiple modules import it, they each get the same object.

The Function Test
-----------------

I created a file called :ref:`singleton_source.py <ape-documentation-singleton-source>` that creates a function called get that creates and returns an instance of the ``SingletonTest`` class. I then created two files ``test_1.py`` and ``test_2.py`` that get the singletons from the singleton source.

``test_1.py``:

.. literalinclude:: test_1.py
   :emphasize-lines: 3

``test_2.py``:

.. literalinclude:: test_2.py
   :emphasize-lines: 3

::

    from ape.documentation.developer.appendices.explore_singletons.test_1 import t1
    from ape.documentation.developer.appendices.explore_singletons.test_2 import t2
    
    assert t1 is t2
    



Testing Without the Function
----------------------------

I think the reason why the example I saw used the function call was so that you can refresh it, but it seems to me that if you aren't going to, you should just be able to create an instance in the module without using a function. Using the same modules as above:

``test_1.py``:

.. literalinclude:: test_1.py
   :emphasize-lines: 5

``test_2.py``:

.. literalinclude:: test_2.py
   :emphasize-lines: 5


::

    from ape.documentation.developer.appendices.explore_singletons.test_1 import test_1
    from ape.documentation.developer.appendices.explore_singletons.test_2 import test_2
    
    assert test_1 is test_2
    



I think I'll use the second version for the plugins.