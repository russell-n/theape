Runfunc
=======

::

    # python standard library
    from trace import Trace
    
    from test_class import TestExec
    



It looks like I had to pass in strings because I used the ``run`` method. To use an object you use ``runfunc``.

::

    trace = Trace()
    t = TestExec()
    try:
        trace.runfunc(t.run_this_and_that)
    except NameError:
        print NameError  
    

::

     --- modulename: test_class, funcname: run_this_and_that
    test_class.py(17):         self.run_this()
     --- modulename: test_class, funcname: run_this
    test_class.py(6):         x = 1
    test_class.py(7):         y = 2
    test_class.py(8):         self.z = x + y
    test_class.py(9):         return
    test_class.py(18):         self.run_that()
     --- modulename: test_class, funcname: run_that
    test_class.py(12):         self.x = 1
    test_class.py(13):         self.y = 2
    test_class.py(14):         return
    test_class.py(19):         return
    



Now, pweave doesn't raise an error, so it looks like this is what I should have used in the first place. But now you aren't actually making a call, what about arguments? 

::

    def args_func(a, b, c=3):
        print 'a',a
        print 'b',b
        print 'c',c
    
    trace.runfunc(args_func, 1, b=2)
    

::

    a 1
    b 2
    c 3
    



So, it looks like there's some kind of ``*args`` ``**kwargs`` thing going on inside there. If you look at the second output you might notice that it seems more sparse than the first. I think it might be because I define the function in this file, if you run it at the command line the output for both calls looks like this:

.. literalinclude:: runfunc.txt