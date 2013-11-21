
# python standard library
from collections import OrderedDict
import textwrap
import importlib

# this package
from base_plugin import BasePlugin
from ape.parts.dummy.dummy import DummyClass
from ape.parts.dummy.dummy import CrashDummy
from ape.parts.dummy.dummy import HangingDummy


DESCRIPTION = """{bold}DummyClass{reset} logs its calls and then returns. It is meant to be used as changes are made to the infrastructure so that the {blue}Ape{reset} can be tested without using any other components."""
EXAMPLES = """{bold}dummy(){reset}"""
NOTE = "The {bold}DummyClass{reset} will change as the infrastructure changes. In particular the building and testing of plugins and components will likely evolve once real plugins are created."


output_documentation = __name__ == '__builtin__'


class Dummy(BasePlugin):
    """
    A plugin to test the infrastructure (a no-op)
    """
    def __init__(self, *args, **kwargs):
        super(Dummy, self).__init__(*args, **kwargs)
        return

    @property
    def sections(self):
        """
        An ordered dict for the help page
        """
        if self._sections is None:
            bold = "{bold}"
            reset = '{reset}'
            
            self._sections = OrderedDict()
            self._sections['Name'] = (bold + 'DummyClass' + reset +
                                        ' -- a no-op')
            self._sections['Description'] = DESCRIPTION
            self._sections['Example'] = EXAMPLES
            self._sections['Note'] = NOTE
        return self._sections

    @property
    def product(self):
        """
        builds and returns a DummyClass

        :precondition: self.configuration map has been set
        """
        if self._product is None:
            kwargs = dict(self.configuration.items(section='DUMMY',
                                                   optional=True,
                                                   default={}))
            self._product = DummyClass(**kwargs)
        return self._product

    def fetch_config(self):
        """
        prints a message saying there is no configuration
        """
        print textwrap.dedent("""
        [DUMMY]
        # the dummy will take anything you set here and log it
        any_arbitrary_option = any_arbitrary_value
        another_option = another_value""")
        return
# end class Dummy


class CrashTestDummy(BasePlugin):
    """
    A plugin to test the infrastructure by crashing
    """
    def __init__(self, *args, **kwargs):
        super(CrashTestDummy, self).__init__(*args, **kwargs)
        return

    @property
    def sections(self):
        """
        An ordered dict for the help page
        """
        if self._sections is None:
            bold = "{bold}"
            reset = '{reset}'
            
            self._sections = OrderedDict()
            self._sections['Name'] = (bold + 'CrashTestDummy' + reset +
                                        ' -- a crashing module')
            self._sections['Description'] = (DESCRIPTION.replace('DummyClass',
                                                                'CrashTestDummy') +
                "\It takes an error to raise as an argument and raises it when called.")
            self._sections['Example'] = EXAMPLES.replace('dummy',
                                                         'crashtestdummy')
            self._sections['Note'] = NOTE
        return self._sections

    @property
    def product(self):
        """
        builds and returns a CrashTestDummy

        :precondition: self.configuration map has been set
        :return: CrashTestDummy
        """
        if self._product is None:
            # get the random inputs and create a keyword-argument- dictionary
            kwargs = dict(self.configuration.items(section='CRASHTESTDUMMY',
                                                   optional=True,
                                                   default={}))

            # see if the user specified an error-module
            error_module = self.configuration.get(section='CRASHTESTDUMMY',
                                                  option='error_module',
                                                  optional=True,
                                                  default=None)
            if error_module is None:
                # nope, choose the default
                error_module = 'exceptions'
                error = 'Exception'
            else:
                error = self.configuration.get(section='CRASHTESTDUMMY',
                                               option='error',
                                               optional=False)
            module = importlib.import_module(error_module)
            err = getattr(module, error)
            kwargs['error'] = err
            message = self.configuration.get(section='CRASHTESTDUMMY',
                                             option='error_message',
                                             optional=True,
                                             default="Die! Die! My Darling!")
            kwargs['error_message'] = message

            # this is the method that raises the error
            function = self.configuration.get(section='CRASHTESTDUMMY',
                                              option='function',
                                              optional=True,
                                              default=CrashDummy.CALL)
            self._product = CrashDummy(**kwargs)
        return self._product

    def fetch_config(self):
        """
        prints a message saying there is no configuration
        """
        print textwrap.dedent("""
        [CRASHTESTDUMMY]
        # the dummy will take anything you set here and log it
        any_arbitrary_option = any_arbitrary_value
        another_option = another_value

        # but these will set the error to raise
        # if these are missing will default to Exception
        error_message = AUUUUUUUGGGGGHHHHHHH
        error_module = exceptions
        error = RuntimeError

        # to have it crash somewhere specific in the component interface
        # can be any attribute you want to call
        # e.g. function = umma will crash if dummy.umma() is called or dummy.umma
        function = __call__""")
        return
# end class CrashTestDummy


class StuckDummy(BasePlugin):
    """
    A plugin to test the infrastructure by hanging
    """
    def __init__(self, *args, **kwargs):
        super(StuckDummy, self).__init__(*args, **kwargs)
        return

    @property
    def sections(self):
        """
        An ordered dict for the help page
        """
        if self._sections is None:
            bold = "{bold}"
            reset = '{reset}'
            
            self._sections = OrderedDict()
            self._sections['Name'] = (bold + 'StuckDummy' + reset +
                                        ' -- a stuck (hanging) module')
            self._sections['Description'] = (DESCRIPTION.replace('DummyClass',
                                                                'StuckDummy') +
                "Sleeps for three years at a time in an infinite loop.")
            self._sections['Example'] = EXAMPLES.replace('dummy',
                                                         'stuckdummy')
            self._sections['Note'] = NOTE
        return self._sections

    @property
    def product(self):
        """
        builds and returns a HangingDummy

        :precondition: self.configuration map has been set
        """
        if self._product is None:
            # get the random inputs and create a keyword-argument- dictionary
            kwargs = dict(self.configuration.items(section='STUCKDUMMY',
                                                   optional=True,
                                                   default={}))

            self._product = HangingDummy(**kwargs)
        return self._product

    def fetch_config(self):
        """
        prints a message saying there is no configuration
        """
        print textwrap.dedent("""
        [HANGINGDUMMY]
        # the dummy will take anything you set here and log it
        any_arbitrary_option = any_arbitrary_value
        another_option = another_value
        """)
        return
# end class HangingDummy
