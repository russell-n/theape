CountCallers
============



This is a test of the ``countcallers`` option.

::

    t = TestExec()
    trace = Trace(countcallers=1)
    try:
        trace.run('t.run_this_and_that()')
        print "COUNTCALLERS"
    except NameError:
        print NameError
    

::

    <type 'exceptions.NameError'>
    



.. literalinclude:: countcallers.txt

Once again it seems to disable the tracing.
