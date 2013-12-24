The Singleton Source
====================

.. _ape-documentation-singleton-source:

This will actually create the singleton.

::

    class SingletonTest(object):
        def __init__(self):
            self.x = 'y'
            return
    
    

::

    def get():
        if get.test is None:
            get.test = SingletonTest()
        return get.test
    
    get.test = None
    test_instance = SingletonTest()
    
    



The idea came from:

Summerfield, Mark. "Python in Practice: Create Better Programs Using Concurrency, Libraries, and Patterns: Safari Books Online." Python in Practice: Create Better Programs Using Concurrency, Libraries, and Patterns: Safari Books Online. Addison-Wesley Professional, 19 Aug. 2013. Web. 18 Dec. 2013. <http://my.safaribooksonline.com/book/programming/python/9780133373271>.
