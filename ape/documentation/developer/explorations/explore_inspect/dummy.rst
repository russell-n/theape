The Dummy Module
================

.. _inspect-dummy-module::
.. currentmodule:: ape.documentation.appendices.inspect.dummy
This is a module created for the inspect exploration.
::

    """
    This is the Dummy Module for the `inspect` exploration.
    """
    
    



A Dummy Class
-------------

To get started a dummy class will be created that does nothing.

.. autosummary::
   :toctree: api

   DummyClass

::

    class DummyClass(object):
        """
        This is a dummy class that inherits from `object`
        """
        def __init__(self, a=None):
            """
            The DummyClass Constructor
    
            :param:
    
             - `a`: anything, this is a dummy
            """
            self.a = a
            return
    
        def a_tuple(self):
            """
            Puts self.a in a tuple and returns it
    
            :return: (self.a, )
            """
            return (self.a,)
    
        def convoluted(self, a, b=5, c='9', d=None):
            """
            This is a method with a lot of args that do nothing
            """
            return
    # end class DummyClass    
    



Now Another Class
-----------------

Since my goal is to use this to discover classes, I will add an inheriting class.

.. uml::

   AnotherClass -|> DummyClass

::

    class AnotherClass(DummyClass):
        """
        A 'nother Class
        """
        def __init__(self, *args, **kwargs):
            """
            AnotherClass constructor
            """
            super(AnotherClass, self).__init__(*args, **kwargs)
            return
    
    



A Plugin Example
----------------

I intend to use this to allow user-level components to be added to the ArachneApe, so there will probably be something like this.

::

    class PluginBase(object):
        """
        A base plugin
        """
        __metaclass__ = ABCMeta
        @abstractproperty
        def help_string(self):
            return
    
        @abstractproperty
        def product(self):
            return
    
        @abstractproperty
        def config(self):
            return        
    



.. uml::

   ConcretePlugin -|> PluginBase
   
::

    class ConcretePlugin(PluginBase):
        """
        A ConcretePlugin
        """
        def __init__(self):
            super(ConcretePlugin, self).__init__()
            return
    
        @property
        def help_string(self):
            """
            Some kind of help string (maybe the help should be the docstring)
            """
            return """
            Now is the winter of our disconcent.
            """
    
        @property
        def product(self):
            """
            This is where the built component should go
            """
            return '0'
    
        @property
        def config(self):
            """
            An example config snippet (does it need to be a property?)
            """
            return """
            [CONCRETE]
            zero = 0
            """
    

