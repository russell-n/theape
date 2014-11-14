The Docopt Test
===============

Contents:

    * :ref:`Usage <docoptest-usage>`
    * :ref:`Arguments <docoptest-arguments>`
    * :ref:`Options <docoptest-options>`

.. _docoptest-usage:
    
Usage
-----

The most basic way to create a doc-opt is to give it one line starting with `Usage: <command>` and ending with an empty line.

::

    usage = """Usage: docoptest
    
    """
    
    



This gets passed to the `docopt` function along with the arguments.

.. currentmodule:: docopt
.. autosummary::
   :toctree: api

   docopt
   

::

    import docopt
    
    output = docopt.docopt(doc=usage, argv=[])
    print output
    
    

::

    {}
    
    



Not very exciting. There are three elements that can follow the command:

   * arguments
   * options
   * commands

.. note:: The `docoptest` command doesn't exist, `docopt` acts only as a argument-parser.

.. '

.. _docoptest-arguments:

Arguments
---------

*Arguments* are positional arguments that are specified as either upper-case or with brackets.

::

    usage = """Usage: docoptest SOMEARGUMENT
                      docoptest SOMEARGUMENT <some-other-argument>
    
    """
    
    output = docopt.docopt(doc=usage, argv=["cowboy"])
    print output
    
    

::

    {'<some-other-argument>': None,
     'SOMEARGUMENT': 'cowboy'}
    
    

::

    output = docopt.docopt(doc=usage, argv="cowboy bob".split())
    print output
    
    

::

    {'<some-other-argument>': 'bob',
     'SOMEARGUMENT': 'cowboy'}
    
    



.. _docoptest-options:

Options
-------

Options are declared on a `Usage` line but defined in the `Options` section below the usage lines.

::

    usage = """Usage: docoptest --number=<count>
    
    """
    output = docopt.docopt(doc=usage, argv="--number 2".split())
    print output
    
    

::

    {'--number': '2'}
    
    



If the option is optional, put it in brackets. It will default to None, if you want a value specify it in the `Options`.

::

    usage="""Usage: docoptest [--number=<count>]
    
    Options:
    
        -n, --number <count>  Some number. [default: 3]
        
    """
    
    output = docopt.docopt(doc=usage, argv=[])
    print output
    
    

::

    {'--number': '3'}
    
    



.. note:: You can separate the short and long options using either a comma or a single-space. The description (`Some number` in the previous example) has to be preceded by **2** spaces.

.. note:: You indicate an option description line by making the first non-space character a `-` (e.g. ``-n`` in the previous example).

You can also put other text before the usage line to make things clearer.

::

    usage="""Manatee
    
    An optional option example.
    
    Usage: docoptest [--number=<count>]
    
    Options:
    
        -n , --number <count>  Some number. [default: 3]
        
    """
    
    output = docopt.docopt(doc=usage, argv='-n 8'.split())
    print output
    
    

::

    {'--number': '8'}
    
    



If you have a lot of options you can reduce the `Usage` line two ways -- use ``[options]`` or combined short-options.

::

    usage = """Usage: docoptest [options]
    
        -n, --name <name>  The Name. [default: bob]
    
    """
    print docopt.docopt(doc=usage, argv=[])
    
    

::

    {'--name': 'bob'}
    
    



.. note:: This changes the behavior somewhat -- all options become optional with defaults of None (unless you change the default). Also, if there's an error, the program will only print the `Usage` so it will be less useful for users.

.. '

The other way to shorten it is to smash-together the short-options.

::

    usage = """Usage: docoptest [-lmn]
    
    In this case we're assumng all the options are boolean flags.
    
    Options:
    
        -l, --long    Use long-mode
        -m, --middle  Use middle-mode
        -n, --nunya   None ya
    """
    print docopt.docopt(doc=usage, argv=["-ln"])
    
    

::

    {'--long': True,
     '--middle': False,
     '--nunya': True}
    
    



Required Options and Alternatives
---------------------------------

Parentheses `()` group required options. `|` (logical or) groups alternatives. If you put alternatives in parentheses::

    docoptest (-n | -c)

Then one of the alternatives is required. If you put it in square brackets (`[]`) then 0 or 1 of them is required.

    docoptest [-n | -c]

::

    usage = """Usage: docoptest [-n=<n> | -c=<c>] (-a=<a>) (-x=<x> | -y=<y>)
    
    Options:
    
        -n, --number <n>  Number of things. [default: 12]
        -c, --count <c>   Count of things. [default: 12]
    
        -a, --ant <a>  Ants
        -x, --xray <x>  X-rays
        -y, --yme <y>  Y-Me
        
    """
    
    print docopt.docopt(doc=usage, argv='-a aoeu --yme because'.split())
    
    

::

    {'--ant': 'aoeu',
     '--count': '12',
     '--number': '12',
     '--xray': None,
     '--yme': 'because'}
    
    



I can't give an example of what happens when you leave out a required option because `docopt` just dumps a usage message to standard error and `pweave` doesn't catch it.

Boolean Options
---------------

If you don't supply a destination for the value (using `<>`) the option is assumed to be a boolean flag.

.. '

::

    usage = """Usage: docoptest [options]
    
    Options:
    
        -b, --boolean  Boolean Flag.
    
    """
    print docopt.docopt(doc=usage, argv="-b".split())
    print docopt.docopt(doc=usage, argv=[])
    
    

::

    {'--boolean': True}
    {'--boolean': False}
    
    



Multiple Values
---------------

To specify an option that can take one or more values, use ellipses (...).

::

    usage = """Usage: docoptest [-f <filename>...]
    
    Options:
    
        -f <filename>...     List of file-names to use. [default: ["ape.pie"]]
        
    """
    print docopt.docopt(doc=usage, argv=[])
    print docopt.docopt(doc=usage, argv='-f apple.pie'.split())
    
    

::

    {'-f': ['["ape.pie"]']}
    {'-f': ['apple.pie']}
    
    



.. warning:: This doesn't work like 'nargs', you have to pass in the option-name before each of the values.

.. '

::

    print docopt.docopt(doc=usage, argv='-f apple.pie -f cow.pie'.split())
    
    

::

    {'-f': ['apple.pie', 'cow.pie']}
    
    



It will work like ``nargs`` if you use it as a positional argument instead.

::

    usage = """Usage: docoptest [<filename>...]
    
    """
    print docopt.docopt(doc=usage, argv='apple.pie cow.pie'.split())
    
    

::

    {'<filename>': ['apple.pie', 'cow.pie']}
    
    



Multiple Definitions
--------------------

If you can take multiple valid combinations of parameters, you can list them separately in the doc-string.

::

    usage="""Megilla Gorilla
    
    Usage: megilla [<name>]
           megilla -f
           megilla -bf <name>
    
    I think this means if the user sets the 'b' flag then f and <name> are requ
    ired.
    
    Arguments:
    
        <name>   Some name. [default: Tom]
    
    Options:
    
         -f, --fluid   Use fluids
         -b, --bob     It's Bob
         
    """
    print docopt.docopt(doc=usage, argv=[])
    print docopt.docopt(doc=usage, argv=['-f'])
    print docopt.docopt(doc=usage, argv='-fb Him'.split())
    try:
        print docopt.docopt(doc=usage, argv='-b'.split())
    except docopt.DocoptExit as error:
        print error
    
    

::

    {'--bob': False,
     '--fluid': False,
     '<name>': None}
    {'--bob': False,
     '--fluid': True,
     '<name>': None}
    {'--bob': True,
     '--fluid': True,
     '<name>': 'Him'}
    Usage: megilla [<name>]
           megilla -f
           megilla -bf <name>
    
    



So we can see two things -- The default argument doesn't work and a DocoptExit exception is raised and the usage string is printed if the arguments don't match one of the usage lines.
