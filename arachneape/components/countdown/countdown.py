
# this package
from arachneape.components.dummy.dummy import DummyClass


class CountDown(DummyClass):
    """
    A countdown timer
    """
    def __init__(self, iterations, *args, **kwargs):
        super(CountDown, self).__init__(*args, **kwargs)
        self.iterations = iterations
        return
# end class CountDown
