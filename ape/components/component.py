
# python standard library
from abc import abstractmethod, ABCMeta, abstractproperty
import inspect
import os

# this package
from ape.commoncode.baseclass import BaseClass
from ape.parts.countdown.countdown import CountDown
from ape.commoncode.strings import RESET, BLUE
from ape.commoncode.strings import BOLD, BOLD_THING, RED
from ape.commoncode.crash_handler import try_except
from ape.commoncode.errors import ConfigurationError
from ape.commoncode.code_graphs import module_diagram, class_diagram


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

    @abstractmethod
    def check_rep(self):
        """
        abstract: Representation-check called by composite

        :raise: ConfigurationError if representation invalid
        """
        return

    @abstractmethod
    def clean_up(self):
        """
        abstractmethod: called for Keyboard Interrupts to allow file-closing
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
                 identifier=None,
                 component_category=None,
                 is_root=False):
        """
        Composite Constructor

        :param:

         - `error`: Exception to catch when calling components
         - `error_message`: string for header of error messages
         - `component_category`: label for error messages when reporting component actions
         - `identifier`: something to identify this when it starts the call
         - `is_root`: if True logs summation information
        """
        super(Composite, self).__init__()
        self.error = error
        self.error_message = error_message
        self.identifier = identifier
        self.component_category = component_category
        self.is_root = is_root
        self._logger = None
        self._components = None
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
        self.logger.debug("{b}** Checking the Composite Class Representation **{r}".format(b=BOLD,
                                                                                          r=RESET))
        self.check_rep()
        count_string = "{b}** {l} {{c}} of {{t}} ('{{o}}') **{r}".format(b=BOLD, r=RESET,
                                                                         l=self.component_category)

        # countdown is going to be a plugin too
        #remaining_string = BOLD_THING.format(thing="Estimated Time Remaining:")
        #total_elapsed = BOLD_THING.format(thing='** Total Elapsed Time:')

        self.logger.info("{b}*** {c} Started ***{r}".format(b=BOLD, r=RESET,
                                                             c=self.identifier))
        
        total_count = len(self.components)
        
        self.logger.info("{b}*** Starting {c} ***{r}".format(b=BOLD, r=RESET,
                                                             c=self.component_category))
        
        for count, component in enumerate(self.components):
            self.logger.info(count_string.format(c=count+1,
                                                 t=total_count,
                                                 o=str(component)))
            self.one_call(component)
        #self.logger.info("{b}*** Ending {c}s ***{r}".format(b=BOLD, r=RESET,
        #                                                    c=self.component_category))

        self.logger.info("{b}*** {c} Ended ***{r}".format(b=BOLD, r=RESET,
                                                             c=self.identifier))        
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

            # check all your children
            for component in self.components:
                component.check_rep()

        except AssertionError as error:
            raise ConfigurationError(str(error))
        return

    def clean_up(self, error):
        """
        calls the `clean_up` method on each component
        """
        for component in self.components:
            try:
                component.clean_up(error)
            except AttributeError as error:
                self.logger.debug.error(error)
                self.logger.warning("`clean_up` not implemented in {0}".format(component))
        return

    def __str__(self):
        return ("{2} -- Traps: {0}, "
                "Component: {1}").format(self.error.__name__,
                                         self.component_category,
                                         self.__class__.__name__)
        
#end class Composite


if DOCUMENT_THIS:
    class_diagram_file = class_diagram(class_name="Composite",
                                       filter='OTHER',
                                       module=this_file)
    print ".. image:: {0}".format(class_diagram_file)
