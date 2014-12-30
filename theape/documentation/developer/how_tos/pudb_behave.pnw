Using `pudb` with Behave and Fish
=================================

What is this about?
-------------------

`behave` is a behavior-driven-development (BDD) tool for python that tests whether you have properly implemented the features you have defined in your `features` file(s). In their `tutorial <http://pythonhosted.org/behave/tutorial.html>`_ they tell you how you can set it up so that it will drop into `ipdb` (ipython debugger) when a test fails, but I use `pudb` and the `fish` shell (not `bash`) so this documents what I had to do to get it to work.

How do you do it then?
----------------------

The first thing to do is create a file named `environment.py` in the same folder as the `features` file. Inside of it put the following::

    from distutils.util import strtobool as _bool
    import os
    
    BEHAVE_DEBUG_ON_ERROR = _bool(os.environ.get("BEHAVE_DEBUG_ON_ERROR",
                                                 "no"))
    def after_step(context, step):
        if BEHAVE_DEBUG_ON_ERROR and step.status == 'failed':
            import pudb
            pudb.post_mortem(tb=step.exc_traceback,
                             e_type=None,
                             e_value=None)
        return

This is more-or-less exactly what was in the tutorial except I swapped out `pudb` for `pdb`. This code tells `behave` to run the `pudb.post_mortem` after a step is finished (a step corresponds to one of the functions you define to implement the tests) if the step failed and your shell has an environment variable named `BEHAVE_DEBUG_ON_ERROR` and it is set to something that `strtobool` recognizes as True. This is from the docstring documentation for `strtobool`:

 distutils.util.strtobool(val)
    Convert a string representation of truth to true (1) or false (0).

    * True values are `y`, `yes`, `t`, `true`, `on` and `1`
    * false values are `n`, `no`, `f`, `false`, `off` and `0`
    * Raises **ValueError** if val is anything else.

The 'no' in the ``os.environ.get`` function means that it won't execute by default. To have it run you need to set the environment varible to one of the 'true' values. In fish this would be::

   set -x BEHAVE_DEBUG_ON_ERROR yes

Now when you run behave it will drop into pudb when a test fails.

So, what then?
--------------

Using this has so far been less useful than I thought it would be, since it tends to drop me into the `pyhamcrest` call that failed and although I've managed to step through to the `behave` code I haven't managed to figure out how to get to my own code. It is still useful, though, since `behave` will not stop when it encounters a failed test so this makes it easier to figure out what has failed.

Even though the `pudb-behave` combination is less exciting than I thought it would be, there were several things I learned that I want to document here.

Setting an environment variable in fish
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To set a fish environment variable::

   set -x <variable> <value>

And then unset it::

   set -e <variable>

Python's String to Boolean
~~~~~~~~~~~~~~~~~~~~~~~~~~

I also learned that python has a built in way to translate strings to booleans. This isn't really a hard thing to do, but it was an interesting discovery. I don't think I would have looked in distutils for it.

Using environment variables for debugging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Another interesting thing was the way they used `os.environ` to change the behavior of the code. I normally use command-line flags but this might be a better pattern since it pulls it out of the user interface. I think I'll probably get rid of in in the `environment.py` file since I want it to run pretty much all the time, but it's an interesting pattern anyway.

`pudb's` post_mortem function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Probably the most interesting thing to find out was that `pudb` has a `post_mortem` function. I like `pudb` but it doesn't seem to be well documented. The ``readme`` does say that it displays the same interface as python's `pdb` so I suppose I could just read their documentation, but it seems like one of those things where you have to know what you don't know to know to look for it.

Conclusion
----------

This was a translation of how to set up a post-mortem debugger for behave using `pudb` instead of `ipdb` and `fish` instead of `bash`. It is primarily meant to be a record for me to look at in the future, since I don't set up my `behave` environment on a regular basis. I think the most valuable thing I got out of it was actuall a pattern for setting up debuggers in my own code that I think I'll steal (use).

