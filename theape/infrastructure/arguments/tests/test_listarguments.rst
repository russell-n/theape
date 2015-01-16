Testing the List Arguments
==========================

.. code:: python

    #python standard library
    import unittest
    
    # third party
    from mock import MagicMock, patch
    
    # the ape
    from theape.infrastructure.arguments.listarguments import List,
    ListStrategy
    from theape.infrastructure.arguments.basestrategy import BaseStrategy
    



.. module:: theape.interface.arguments.test.test_listarguments
.. autosummary::
   :toctree: api

   TestList.test_constructor
   TestList.test_modules


.. code:: python

    class TestList(unittest.TestCase):
        def setUp(self):
            self.args = ['list']
            self.arguments = List(args=self.args)
            return
    
        def test_constructor(self):
            """
            Does it build correctly?
            """
            arguments = List(args=['list'])
    
            # inderited default
            self.assertFalse(arguments.pudb)
            return
    
        def test_modules(self):
            """
            Does it get the list of plugin modules?
            """
            # default to empty list
            self.assertEqual([], self.arguments.modules)
    
            # positional arguments
            modules = 'ape bat chameleon'.split()
            self.arguments.reset()
            self.arguments.args = self.args + modules
            self.assertEqual(modules, self.arguments.modules)
            return
    



Testing the List Strategy
-------------------------

.. autosummary::
   :toctree: api

   TestListStrategy.test_constructor
   TestListStrategy.test_function
   TestListStrategy.test_try_except



