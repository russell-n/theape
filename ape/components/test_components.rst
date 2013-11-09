Testing Components
==================

Including the tests in the implementation is making the module-diagrams unreadable so they are moved here.



Testing the Component
---------------------

.. currentmodule:: ape.components.test_components
.. autosummary::
   :toctree: api

   TestComponent.test_bad_component



Testing the Composite
---------------------

.. autosummary::
   :toctree: api

   TestComposite.test_add_component
   TestComposite.test_remove_component
   TestComposite.test_slice
   TestComposite.test_check_rep



Testing the Hortator
--------------------

The Hortator is just an instance of the Composite. This is a check that my idea of how to implement it will work.

.. autosummary::
   :toctree: api

   TestHortator.test_exception



Testing the Operator
--------------------

Like the Hortator, the Operator is just an instance of the Composite, but it should only catch ApeErrors.

.. autosummary::
   :toctree: api

   TestOperator.test_exception

