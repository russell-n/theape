
# python standard library
import unittest

# third-party
try:
    from mock import MagicMock
except ImportError:
    pass

# this package
from ape.commoncode.errors import ApeError, ConfigurationError
from ape.components.component import Component, Composite


class BadComponent(Component):
    def __init__(self):
        return

class BetterComponent(Component):
    def __call__(self):
        return

    def check_rep(self):
        return

class TestComponent(unittest.TestCase):
    def setUp(self):
        self.composite = Composite()
        self.component = BetterComponent()
        return
    
    def test_bad_component(self):
        """
        Does it raise a TypeError if you do not implement the __call__?
        """
        self.assertRaises(TypeError, BadComponent)
        BetterComponent()
        return


class TestComposite(unittest.TestCase):
    def setUp(self):
        self.composite = Composite()
        self.component = BetterComponent()
        return
    
    def test_add_component(self):
        self.composite.add(self.component)
        self.composite.add(self.component)
        self.assertEqual(1, len(self.composite))
        self.assertIn(self.component, self.composite)
        return

    def test_remove_component(self):
        self.composite.add(self.component)
        self.composite.remove(self.component)
        return

    def test_slice(self):
        self.composite.add(self.component)
        # indexing
        self.assertEqual(self.component, self.composite[-1])
        component = BetterComponent()
        self.composite.add(component)
        # slicing
        self.assertEqual([self.component, component], self.composite[:])
        return

    def test_check_rep(self):
        self.composite.error = ApeError
        self.composite.error_message = "Die antwoort ist nicht in die aufreissen."
        self.composite.component_category = "Piltdown Mann"
        # this should not raise an error
        self.composite.check_rep()

        # error cannot be None
        self.composite.error = None
        self.assertRaises(ConfigurationError, self.composite.check_rep)

        # error must be exception
        self.composite.error = Composite
        self.assertRaises(ConfigurationError, self.composite.check_rep)

        self.composite.error = ApeError
        self.composite.error_message = None
        self.assertRaises(ConfigurationError, self.composite.check_rep)

        self.composite.error_message = 'Ausgezeichnet.'
        self.composite.component_category = None
        self.assertRaises(ConfigurationError, self.composite.check_rep)
        return



class TestHortator(unittest.TestCase):
    def setUp(self):
        self.hortator = Composite(error=Exception,
                                  error_message="Operator Crash",
                                  component_category='Operator')
        return

    def test_exception(self):
        bad_operator = MagicMock(side_effect =Exception('bad operator1'))        
        next_operator = MagicMock()
        self.hortator._logger = MagicMock()
        self.hortator.add(bad_operator)
        self.hortator.add(next_operator)
        self.hortator()
        return


class TestOperator(unittest.TestCase):
    def setUp(self):
        self.operator = Composite(error=ApeError,
                                  error_message='Operation Crash',
                                  component_category='Operation')
        self.operator._logger = MagicMock()
        return

    def test_exception(self):
        component = MagicMock(side_effect=ApeError)
        component_2 = MagicMock()
        self.operator.add(component)
        self.operator.add(component_2)
        self.operator()
        # the composite should catch the ApeError and move on to component_2
        component_2.assert_called_with()

        # component_3 raises an Exception that should not be caught
        component_3 = MagicMock(side_effect=Exception)
        self.operator.add(component_3)

        # countdown isn't meant to re-run (bug?)
        self.operator._countdown = None

        self.assertEqual(3, len(self.operator))
        
        # but it should not catch an Exception
        self.assertRaises(Exception, self.operator)
        return
