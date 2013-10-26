
# python standard library
import textwrap

# this (real) package
from ape.plugins.base_plugin import BasePlugin
from ape.parts.dummy.dummy import DummyClass


class FakePlugin(BasePlugin):
    """
    A fake plugin
    """
    def __init__(self, *args, **kwargs):
        super(FakePlugin, self).__init__(*args, **kwargs)
        return

    def fetch_config(self):
        print textwrap.dedent("""
        [FAKEPLUGIN]
        #this is a fake plugin that creates a DummyClass instance
        # anything put in this section will be logged
        # but nothing will be done with it
        """)
        return

    @property
    def product(self):
        """
        Creates a dummy-class instance.
        """
        if self._product is None:
            kwargs = dict(self.configuration.items(section='FAKEPLUGIN',
                                                   optional=True,
                                                   default={}))
            self._product = DummyClass(**kwargs)

        return self._product

    @property
    def sections(self):
        return {}
    


class BrokenPlugin(BasePlugin):
    """
    A broken (fake) plugin
    """
    def __init__(self, *args, **kwargs):
        super(BrokenPlugin, self).__init__(*args, **kwargs)
        return

    def fetch_config(self):
        return

    @property
    def product(self):
        """
        :return: None
        """
        return

    @property
    def sections(self):
        """
        :return: None
        """
        return {'something':1}
    


if __name__ == '__main__':
    fp = FakePlugin()
