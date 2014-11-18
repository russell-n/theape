Countfuncs
==========


Among other things, ``Trace`` takes a ``countfuncs`` (Boolean) value to turn on listing of the functions as the code is run.

::

    t = TestExec()
    trace = Trace(countfuncs=True)
    try:
        trace.run('t.run_this_and_that()')
        print "COUNTFUNCS"
    except NameError:
        print NameError
    

::

    <type 'exceptions.NameError'>
    



.. literalinclude:: countfuncs.txt
   :start-after: END_DEFAULT

Interestingingly, it seems to have disabled the trace. Not what I was expecting.

