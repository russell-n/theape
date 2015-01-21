Exploring Files
===============

Contents:

    * :ref:`Background <exploring-files-background>`

    * :ref:`The file API <exploring-files-api>`

    * :ref:`Implementing the Context Manager <exploring-files-context-manager>`

.. _exploring-files-background:
    
Background
----------

The goal of part of the APE is to create a :ref:`Storage <ape-storage>` class that acts like a file but adds some extra features and allows for the introduction of other classes with the same interface that can be dropped into it. In order to make it easier to decide what to implement, the built-in python `file object <http://docs.python.org/2/library/stdtypes.html#bltin-file-objects>`_ will be used as the starting point. As such, this will be a record of what's in it.

Most of this will be about `file`, which is what you create when using the `open` function:

::

    open(name[, mode[, buffering]]) -> file object
    
    Open a file using the file() type, returns a file object.  This is the
    preferred way to open a file.  See file.__doc__ for further information.
    
    



.. _exploring-files-context-manager:

The Context Manager
-------------------

The file's ``close`` method is automatically called when you use a `context manager <http://www.python.org/dev/peps/pep-0343/>`_ which is apparently the preferred method (although it only seems reasonable when you don't need extended access to a file). In order to support this in a file-like class you need to define an ``__enter__`` and an ``__exit__``.

First -- what if I don't?

.. superfluous '

::

    class FakeFile(object):
        def __init__(self, name):
            self.name = name
            return
    
    try:        
        with FakeFile('cow') as f:
            f.write()
    except AttributeError as error:
        print str(error)
    

::

    __exit__
    



Well, the error message was a little obscure, but I'll add an ``__exit__`` method to fix it.

.. superfluous '

::

    class FakeFile(object):
        def __init__(self, name):
            self.name = name
            return
    
        def __exit__(self):
            return
    
    try:        
        with FakeFile('cow') as f:
            f.write()
    except AttributeError as error:
        print str(error)
    

::

    __enter__
    



Now, an ``__enter__``.

::

    class FakeFile(object):
        def __init__(self, name):
            self.name = name
            return
    
        def __enter__(self):
            return
    
        def __exit__(self):
            return
    
    try:        
        with FakeFile('cow') as f:
            f.write()
    except TypeError as error:
        print str(error)
    

::

    __exit__() takes exactly 1 argument (4 given)
    



Well, it's a different error, so we must be maxing progress. Looking at Fredrick Lundh's `explanation <http://effbot.org/zone/python-with-statement.htm>`_ of the ``with`` statement, it looks like the ``__exit__`` method is being passed some arguments that don't exist in my method definition.

.. superfluous '

::

    class FakeFile(object):
        def __init__(self, name):
            self.name = name
            return
    
        def __enter__(self):
            """Setup the file"""
            self.output = sys.stdout
            return self
    
        def __exit__(self, type, value, traceback):
            """Tear it down"""
            self.output.flush()
            print "{0} is exited".format(self.name)
            return 
    
        def write(self, text):
            self.output.write(text)
            return
    
        def close(self):
            print "{0} is closed".format(self.name)
            self.output.close()
            return
    
    with FakeFile('cow') as f:
        f.write("pie\n")
    

::

    pie
    cow is exited
    



Well, that isn't really a concrete example of much, but it sits here as a reference for what has to be implemented to support context managers.

.. superfluous '

As an aside, python has a way that you can use any file-like object with a context manager, even if it doesn't have the ``__enter__`` and ``__exit__`` methods:

.. superfluous '

::

    from contextlib import closing
    
    class FakeFile(object):
        def __init__(self, name):
            self.name = name
    
        def write(self, text):
            print text
    
        def close(self):
            print "{0} has been closed".format(self.name)
            return
    
    with closing(FakeFile('noexit')) as fake:
        fake.write('ummagumma')
    

::

    ummagumma
    noexit has been closed
    



In this case I'm implementing the file-like object so I should'nt need it, but it's noted here for future use. An interesting thing to note is that the class with ``__enter__`` and ``__exit__`` implemented doesn't call close() while the ``closing`` context manager does, so they are similar but not the same.

.. _exploring-files-flush:

flush
-----

The documentation notes that calling ``file.flush`` flushes the buffer, but this is not the same thing as writing to disk. If that's what you want you would need two calls::

    f.flush()  # flush the file-buffer
    os.fsync() # tell the OS to write the file to the disk

.. superfluous '



.. _exploring-files-api:

The __builtin__.file API
------------------------

Basic things common to all files.

.. currentmodule:: __builtin__
.. autosummary:: 
   :toctree: api

   file
   file.close
   file.flush
   file.fileno
   file.isatty

Methods for reading.

.. autosummary::
   :toctree: api

   file.next
   file.read
   file.readline
   file.readlines
   file.seek
   file.tell

Methods for writing.

.. autosummary::
   :toctree: api

   file.write
   file.writelines

Properties.

.. autosummary::
   :toctree: api

   file.closed
   file.encoding
   file.errors
   file.mode
   file.name
   file.newlines
   file.softspace

