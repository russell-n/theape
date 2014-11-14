The Base Usage String
---------------------

I'll start by trying to reproduce the usage string, taking advantage of the greater flexibility of docopt.

.. '

::

    usage = """The APE
    
    The All-in-one Performance Evaluator.
    
    Usage: ape -h|-v
    
    Optional Arguments:
    
        -h, --help     Print a help message.
        -v, --version  Print the version number.
    
    """
    
    



Help and Version
~~~~~~~~~~~~~~~~

``help`` and ``version`` are special flags that are intercepted by ``docopt`` so you don't have to handle them (using version requires you to pass in the version to the `docopt` function call). Since the ``docopt`` help and version calls force the program to exit, I created a function to trap the exception called catch_exit (otherwise Pweave will quit and this documentation won't get built).

.. '

::

    catch_exit(usage, argv=['-h'])
    

::

    The APE
    
    The All-in-one Performance Evaluator.
    
    Usage: ape -h|-v
    
    Optional Arguments:
    
        -h, --help     Print a help message.
        -v, --version  Print the version number.
    



Without the version set it thinks `-v` is just another option:

::

    print docopt.docopt(doc=usage, argv=['-v'])
    

::

    {'--help': False,
     '--version': True}
    



With the version set `-v` tells it to print the version:

::

    catch_exit(usage, argv=['-v'], version="alpha.beta.gamma")
    
    

::

    alpha.beta.gamma
    
    



I defined the options as mutually exclusive (``-h | -v``), what happens if we pass in both flags?

::

    catch_exit(usage, argv='--help --version'.split(), version='abc')
    
    

::

    The APE
    
    The All-in-one Performance Evaluator.
    
    Usage: ape -h|-v
    
    Optional Arguments:
    
        -h, --help     Print a help message.
        -v, --version  Print the version number.
    
    



It unexpectedly accepts the `help` option and ignores the `version` option. Is it the ordering that matters?

::

    catch_exit(usage, argv='-v -h'.split())
    
    

::

    The APE
    
    The All-in-one Performance Evaluator.
    
    Usage: ape -h|-v
    
    Optional Arguments:
    
        -h, --help     Print a help message.
        -v, --version  Print the version number.
    
    



Apparently `help` intercepts the other options.

.. _docopt-reproducingape-base-options:

Base Options
------------

Now that help and version are out of the way, let's add some options for the ape to interpret.

.. '

Logging Levels
~~~~~~~~~~~~~~

::

    usage = """APE
    Usage: ape -h | -v
           ape --debug | --silent
    
    Help Options:
    
        -h, --help     Display this help message and quit.
        -v, --version  Display the version number and quit.
        
    Ape Options:
    
        --debug   Set logging level to DEBUG.
        --silent  Set logging level to ERROR.
    
    """
    print docopt.docopt(doc=usage, argv=["--silent"])
    

::

    {'--debug': False,
     '--help': False,
     '--silent': True,
     '--version': False}
    



As expected, the options default to `False` and since we passed in the ``--silent`` only `silent` in the returned dictionary was set to `True`. What if we pass both silent and debug?

::

    print catch_exit(usage, argv='--silent --debug'.split())
    
    

::

    Usage: ape -h | -v
           ape --debug | --silent
    
    



It looks like with the exception of cases where `help` is involved, `docopt` will enforce the 0 or 1 cardinality for the alternative options -- you can either choose one or leave it out altogether, but you can't pick more than one of them.

.. '

Interactive Debugging
~~~~~~~~~~~~~~~~~~~~~

What about adding interactive debugging options (`pudb` or `pdb`)?

::

    usage = """APE
    Usage: ape -h | -v
           ape [--debug | --silent] [--pudb | --pdb]
    
    Help Options:
    
        -h, --help     Display this help message and quit.
        -v, --version  Display the version number and quit.
        
    Ape Options:
    
        --debug   Set logging level to DEBUG.
        --silent  Set logging level to ERROR.
    
    """
    
    



I'll try setting both logging and debugging, which are both optional and not mutually exclusive.

.. '

::

    print docopt.docopt(doc=usage, argv="--silent --pudb".split())
    
    

::

    {'--debug': False,
     '--help': False,
     '--pdb': False,
     '--pudb': True,
     '--silent': True,
     '--version': False}
    
    



As expected, the dictionary entries for ``--silent`` and ``--pudb`` are True and and all the others are False.

Trace and Callback
~~~~~~~~~~~~~~~~~~

The last of the top-level options are `trace` and `callback` (which I don't remember as being particularly useful). Does it make sense to be able to set an interactive debugger when using trace or callback? Probably not, but what about the logging level? Maybe. I'll say yes for now.

::

    usage = """APE
    Usage: ape -h | -v
           ape [--debug | --silent] [--pudb | --pdb]
           ape  [--debug | --silent] [--trace] [--callback]
    
    Help Options:
    
        -h, --help     Display this help message and quit.
        -v, --version  Display the version number and quit.
        
    Ape Options:
    
        --debug   Set logging level to DEBUG.
        --silent  Set logging level to ERROR.
    
    """
    print docopt.docopt(doc=usage, argv="--trace --debug --callback".split())
    
    

::

    {'--callback': True,
     '--debug': True,
     '--help': False,
     '--pdb': False,
     '--pudb': False,
     '--silent': False,
     '--trace': True,
     '--version': False}
    
    



If you look at the dictionary that was returned you can see that ``--trace, --debug`` and ``--callback`` were set to True and all the others to False, so it's still working as expected. We now have three usage lines that each takes a different set of options, what happens if you mix up options from two different lines?

.. '

::

    print catch_exit(usage, argv='--callback --pudb')
    
    

::

    Usage: ape -h | -v
           ape [--debug | --silent] [--pudb | --pdb]
           ape  [--debug | --silent] [--trace] [--callback]
    
    



It looks like it enforces the usage strings so your arguments have to match one of the usage-lines: `--pudb` isn't offered on the same line that has `--callback` so it (docopt) prints the usage message and quits.


