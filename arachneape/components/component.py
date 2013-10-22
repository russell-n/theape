
# python standard library
from abc import abstractmethod, ABCMeta, abstractproperty
import inspect
import os

# this package
from arachneape.commoncode.baseclass import BaseClass
from arachneape.parts.countdown.countdown import CountDown
from arachneape.commoncode.strings import RESET, BLUE
from arachneape.commoncode.strings import BOLD, BOLD_THING, RED
from arachneape.commoncode.crash_handler import try_except
from arachneape.commoncode.errors import ConfigurationError
from arachneape.commoncode.code_graphs import module_diagram, class_diagram


DOCUMENT_THIS = __name__ == '__builtin__'


if DOCUMENT_THIS:
    this_file = os.path.join(os.getcwd(), 'component.py')
    module_diagram_file = module_diagram(module=this_file, project='composite')
    print ".. image:: {0}".format(module_diagram_file)


class Component(BaseClass):
    """
    A base-class for Composite and Leaf
    """
    __metaclass__ = ABCMeta
    def __init__(self):
        super(Component, self).__init__()
        self._logger = None
        return

    @abstractmethod
    def __call__(self):
        """
        abstractmethod that will be the main invocation when implememented
        """
        return


if DOCUMENT_THIS:
    class_diagram_file = class_diagram(class_name="Component",
                                       filter='OTHER',
                                       module=this_file)
    print ".. image:: {0}".format(class_diagram_file)


class Composite(Component):
    """
    A Composite to hold and execute Components
    """
    def __init__(self, error=None, error_message=None,
                 component_category=None, countdown=None,
                 is_root=False):
        """
        Composite Constructor

        :param:

         - `error`: Exception to catch when calling components
         - `error_message`: string for header of error messages
         - `countdown`: A pre-built countdown timer
         - `component_category`: label for error messages when reporting component actions
         - `is_root`: if True logs summation information
        """
        super(Composite, self).__init__()
        self.error = error
        self.error_message = error_message
        self.component_category = component_category
        self.is_root = is_root
        self._logger = None
        self._components = None
        self._countdown = None
        return

    @property
    def components(self):
        """
        The list of components
        """
        if self._components is None:
            self._components = []
        return self._components

    def add(self, component):
        """
        appends the component to self.components

        :param:

         - `component`: A Component

        :postcondition: component appended to components
        """
        # using is instead of in in case __eq__ overriden
        for existing_component in self.components:
            if component is existing_component:
                return
        self.components.append(component)
        return

    def remove(self, component):
        """
        Removes the component from the components (if it was there)
        """
        try:
            self.components.remove(component)
        except ValueError as error:
            self.logger.debug(error)
        return

    def __iter__(self):
        """
        Iterates over the components
        """
        for component in self.components:
            yield component

    def __len__(self):
        """
        Counts the components

        :return: count of components
        """
        return len(self.components)

    def __getitem__(self, index):
        """
        gets slice or index of components
        """
        return self.components[index]

    @property
    def countdown(self):
        """
        A Countdown Timer
        """
        if self._countdown is None:
            self._countdown = CountDown(iterations=len(self.components))
        return self._countdown

    @try_except
    def one_call(self, component):
        """
        Calls the  component (pulled out into a method to catch the exceptions)
        """
        component()
        return

    def __call__(self):
        """
        The main interface -- starts components after doing a check_rep

        """
        self.check_rep()
        self.countdown.start()
        count_string = "{b}** {l} {{c}} of {{t}} ('{{o}}') **{r}".format(b=BOLD, r=RESET,
                                                                         l=self.component_category)

        remaining_string = BOLD_THING.format(thing="Estimated Time Remaining:")
        total_elapsed = BOLD_THING.format(thing='** Total Elapsed Time:')
        
        total_count = len(self.components)
        self.logger.info("{b}*** Starting {c} ***{r}".format(b=BOLD, r=RESET,
                                                             c=self.component_category))
        
        for count, component in enumerate(self.components):
            if not self.countdown.time_remaining:
                self.logger.info('Time Exceeded, quitting')
                break

            self.logger.info(count_string.format(c=count+1,
                                                 t=total_count, o=str(component)))
            self.logger.info(remaining_string.format(value=self.countdown.remaining))
            
            self.one_call(component)
            self.countdown.next_iteration()
        self.logger.info("{b}*** Ending {c}s ***{r}".format(b=BOLD, r=RESET,
                                                            c=self.component_category))
        if self.is_root:
            self.logger.info(total_elapsed.format(value=self.countdown.elapsed))        
        return

    def check_rep(self):
        """
        Checks the representation invariant

        :raise: ConfigurationError
        """
        try:
            assert inspect.isclass(self.error),(
                "self.error must be an exception, not {0}".format(self.error))
            assert issubclass(self.error, Exception),(
                "self.error needs to be an exception, not {0}".format(self.error))
            assert self.error_message is not None, (
                "self.error_message must not be None")
            assert self.component_category is not None, (
                "self.component_category must not be None")

        except AssertionError as error:
            raise ConfigurationError(str(error))
        return
#end class Composite


if DOCUMENT_THIS:
    class_diagram_file = class_diagram(class_name="Composite",
                                       filter='OTHER',
                                       module=this_file)
    print ".. image:: {0}".format(class_diagram_file)


# python standard library
import unittest

# third-party
try:
    from mock import MagicMock
except ImportError:
    pass

# this package
from arachneape.commoncode.errors import ApeError


class BadComponent(Component):
    def __init__(self):
        return

class BetterComponent(Component):
    def __call__(self):
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
