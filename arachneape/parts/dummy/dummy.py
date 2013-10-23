
# this package
from arachneape.commoncode.baseclass import BaseClass
from arachneape.commoncode.strings import CREATION, ARGS, KWARGS
from arachneape.commoncode.strings import CALLED_ON, CALLED, NOT_IMPLEMENTED

# this module
from callclass import CallClass


output_documentation = __name__ == '__builtin__'


class DummyClass(BaseClass):
    """
    The Dummy Class does nothing
    """
    def __init__(self, *args, **kwargs):
        """
        Dummy class constructor
        """
        super(DummyClass, self).__init__()
        self._logger = None
        self.logger.info(CREATION.format(thing=self))
        self.logger.info(ARGS.format(value=args))
        self.logger.info(KWARGS.format(value=kwargs))
        for name, value in kwargs.items():
            setattr(self, name, value)
        return

    def __call__(self, *args, **kwargs):
        """
        Logs the fact that it was called
        """
        self.logger.info(CALLED.format(thing=self))
        self.logger.info(ARGS.format(value=args))
        self.logger.info(KWARGS.format(value=kwargs))
        return

    def __str__(self):
        """
        Returns the class name
        """
        return self.__class__.__name__

    def __getattr__(self, attribute):
        """
        To catch unimplemented parts of the class and log them
        """
        self.logger.info(CALLED_ON.format(attribute=attribute,
                                          thing=self))
        return CallClass(NOT_IMPLEMENTED.format(thing=self))
# end class Dummy    


class CrashDummy(DummyClass):
    """
    A dummy that crashes
    """
    def __init__(self, error, error_message="CrashDummy is crashing.",
                 *args, **kwargs):
        super(CrashDummy, self).__init__(*args, **kwargs)
        self.error = error
        self.error_message = error_message
        return

    def __call__(self, *args, **kwargs):
        super(CrashDummy, self).__call__(*args, **kwargs)
        raise self.error(self.error_message)
        return
    


# python standard library
import unittest

# third-party
try:
    from mock import MagicMock
except ImportError:
    pass    


class TestCrashDummy(unittest.TestCase):
    def setUp(self):
        self.dummy = CrashDummy(error=RuntimeError, other='other')
        self.dummy._logger = MagicMock()
        return

    def test_crash(self):
        self.assertRaises(RuntimeError, self.dummy)


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


if __name__ == '__main__':
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
