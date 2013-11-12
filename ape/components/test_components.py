
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
from ape.commoncode.baseclass import RED_ERROR


class BadComponent(Component):
    def __init__(self):
        return

class StillBadComponent(Component):
    def __init__(self):
        return

    def __call__(self):
        return
    
class BetterComponent(Component):
    def __call__(self):
        return

    def check_rep(self):
        return

    def close(self):
        return

class EvilComponent(object):
    def __init__(self):
        return

class TestComponent(unittest.TestCase):
    def setUp(self):
        self.composite = Composite()
        self.component = BetterComponent()
        return
    
    def test_bad_component(self):
        """
        Does it raise a TypeError if you do not implement the __call__ or check_rep?
        """
        self.assertRaises(TypeError, BadComponent)
        self.assertRaises(TypeError, StillBadComponent)
        BetterComponent()
        return


class TestComposite(unittest.TestCase):
    def setUp(self):
        self.composite = Composite()
        self.component = BetterComponent()
        return
    
    def test_add_component(self):
        """
        Can you add a component once and only once?
        """
        self.composite.add(self.component)
        self.composite.add(self.component)
        self.assertEqual(1, len(self.composite))
        self.assertIn(self.component, self.composite)
        return

    def test_remove_component(self):
        """
        Can you remove a component you added?
        """
        self.composite.add(self.component)
        self.composite.remove(self.component)
        self.composite.remove(self.component)
        return

    def test_slice(self):
        """
        Can you use the siice syntax to get a subset ofe the components?
        """
        self.composite.add(self.component)
        # indexing
        self.assertEqual(self.component, self.composite[-1])
        component = BetterComponent()
        self.composite.add(component)
        # slicing
        self.assertEqual([self.component, component], self.composite[:])
        return

    def test_check_rep(self):
        """
        Does check_rep check the Composite and all its components?
        """
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

    def test_evil_component(self):
        """
        Does a mis-implemented component raise an ApeError on call and a warning for others?
        """
        evil = EvilComponent()
        self.composite.add(evil)
        self.composite.error = ApeError
        self.composite.error_message = 'this is an error'
        self.composite.component_category = 'memyselfandi'

        # if check_rep is not implemented, just warn
        mock_logger = MagicMock()
        self.composite._logger = mock_logger
        self.composite.check_rep()
        message = RED_ERROR.format(error="'EvilComponent' hasn't implemented the 'check_rep' method.",
                                   message="Thanks for the sour persimmons, cousin.")
        mock_logger.error.assert_called_with(message)
        
        # if close not implemented just emit message
        self.composite.close()
        mock_logger.warning.assert_called_with("'EvilComponent' hasn't implemented the 'close' method. We hate him.")
        # if the call is not implemented, raise an ApeError to kill the operation
        self.assertRaises(ApeError, self.composite())
        return



class TestHortator(unittest.TestCase):
    def setUp(self):
        self.hortator = Composite(error=Exception,
                                  error_message="Operator Crash",
                                  component_category='Operator')
        return

    def test_exception(self):
        """
        Does the hortator's call catch Exceptions so the Ape doesn't crash and move to the next operator?
        """
        bad_operator = MagicMock(side_effect = Exception('bad operator1'))        
        next_operator = MagicMock()
        self.hortator._logger = MagicMock()
        self.hortator.add(bad_operator)
        self.hortator.add(next_operator)
        self.hortator()
        next_operator.assert_called_with()
        return


class TestOperator(unittest.TestCase):
    def setUp(self):
        self.operator = Composite(error=ApeError,
                                  error_message='Operation Crash',
                                  component_category='Operation')
        self.operator._logger = MagicMock()
        return

    def test_exception(self):
        """
        Does the operator catch ApeErrors but not Exceptions?
        """        
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
