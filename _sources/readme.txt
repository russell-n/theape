The APE (Read Me)
=================



The `All-Purpose Experimenter` is a plugin-based system meant to create a unified front-end for different device-related testing. The stable documentation is on `pythonhosted <http://pythonhosted.org//theape/>`_, and the documentation for the on-going updates are on `github <https://rsnakamura.github.io/theape/>`_.

Installation
------------

If you have the repository you can install it by using the ``setup.py`` file.

.. code:: bash

   python setup.py install

Alternately you can pull it from PyPi.

.. code:: bash

   pip install theape

If you are installing it system-wide you will probably have to prefix this and other install commands with ``sudo``.


Command Line Help
-------------

The APE has some command-line help.

.. code:: bash

   theape -h


.. code::

    APE (the all-purpose-evaluator)
    
    Usage: ape -h | -v
           ape [--debug|--silent] [--pudb|--pdb] <command> [<argument>...]
           ape [--debug|--silent] [--trace|--callgraph] <command> [<argument>...]
    
    Help Options:
    
        -h, --help     Display this help message and quit.
        -v, --version  Display the version number and quit.
        
    Logging Options:
    
        --debug   Set logging level to DEBUG.
        --silent  Set logging level to ERROR.
    
    Debugging Options:
    
        --pudb       Enable the `pudb` debugger (if installed)
        --pdb        Enable the `pdb` (python's default) debugger
        --trace      Enable code-tracing
        --callgraph  Create a call-graph of for the code
    
    Positional Arguments:
    
        <command>      The name of a sub-command (see below)
        <argument>...  One or more options or arguments for the sub-command
        
    Available Sub-Commands:
    
        run    Run a plugin
        fetch  Fetch a sample configuration-file
        help   Display more help
        list   List known plugins
        check  Check a configuration
    
    To get help for a sub-command pass `-h` as the argument. e.g.:
    
        ape run -h
    
    



I don't have much user documentation set up yet, so I'll just dump the sub-commands' help.

.. '

Run Sub-Command
~~~~~~~~~~~~~~~


.. code::

    `run` sub-command
    
    Usage: theape run -h
           theape run [<configuration>...]
    
    Positional Arguments:
    
        <configuration>   0 or more configuration-file names [default: ape.ini]
    
    Options;
    
        -h, --help  This help message.
    
    



The ``run`` sub-command grabs the configuration files and runs the plugins listed.

Fetch Sub-Command
~~~~~~~~~~~~~~~~~


.. code::

    fetch subcommand
        
    usage: ape fetch -h
           ape fetch [<name>...]  [--module <module> ...] 
    
    positional arguments:
        <name>                         List of plugin-names (default=['Ape'])
    
    optional arguments:
        -h, --help                     Show this help message and exit
        -m, --module <module> ...      Non-ape modules
    
    



The ``fetch`` sub-command dumps the `theape` sample configuration to standard-out. If you pass in one or more plugin names it will output their sample configurations instead. The intent is for the output to be re-directed to a file for editing or to dump it to the screen if you just want to see the options. You can combine the Ape's configuration with other plugins' configurations by using `Ape` explicitly::

    theape fetch Ape Sleep Dummy

Right nom there aren't any interesting ones built into the Ape, as I'm focusing on building plugin-adapters for some code that I don't own, but external plugin-adapters can be referenced using the ``-m`` or ``--module`` option. Note that it's a module name, not a package name that has to be passed in. If, for example, there is an Ape-plugin named ``Ping`` in a ``plugins`` file within a package named ``apeplugins``, you should be able to get its sample configuration like this::

    theape fetch --module apeplugins.plugins Ping

The Help Sub-Command
~~~~~~~~~~~~~~~~~~~~


.. code::

    `help` sub-command
    
    usage: ape help -h
           ape help [-w WIDTH] [--module <module>...] [<name>]
    
    positional arguments:
        <name>                A specific plugin to inquire about [default: Ape].
    
    optional arguments:
        -h, --help            show this help message and exit
        -w , --width <width>  Number of characters to wide to format the page. [default: 80]
        -m, --module <module>     non-ape module with plugins
        
    
    



    The ``help`` sub-command displays the help strings provided by the plugins. They are meant to be man-page-like so they are formatted and output to less. As with ``fetch`` you need to specify any non-ape modules.

The List Sub-Command
~~~~~~~~~~~~~~~~~~~~


.. code::

    list subcommand
    
    usage: ape list -h
           ape list [<module> ...]
    
    Positional Arguments:
      <module> ...  Space-separated list of importable module with plugins
    
    optional arguments:
    
      -h, --help                 Show this help message and exit
    
    



The ``list`` subcommand prints out any Ape Plugins that are found. Like the ``help`` and ``fetch`` sub-commands the ``list`` needs to be told about any external plugins. Unlike them it takes them as positional arguments (not using the ``-m`` option). This was meant to reduce typing, although I might change this to be more consistent later.

The Check Sub-Command
~~~~~~~~~~~~~~~~~~~~~


.. code::

    `check` sub-command
    
    usage: ape check -h
           ape check  [<config-file-name> ...] [--module <module> ...]
    
    Positional Arguments:
    
        <config-file-name> ...    List of config files (e.g. *.ini - default='['ape.ini']')
    
    optional arguments:
    
        -h, --help                  Show this help message and exit
        -m, --module <module>       Non-ape module with plugins
    
    



This sub-command builds the configuration and calls the ``check_rep`` method of each of the plugins. It is meant to validate your configuration without running the test.

Building the Written Documentation
----------------------------------

The APE was written in a literate-programming style with Pweave. The ``theape`` folder serves as both the python package code and as a `sphinx` source repository. If you want to compile the documentation you will at a minimum need `Sphinx <http://sphinx-doc.org/>`_, `alabaster <https://pypi.python.org/pypi/alabaster>`_ , and `sphinxcontrib-plantuml <https://pypi.python.org/pypi/sphinxcontrib-plantuml>`_. To get the ``sphinxcontrib-plantuml`` also requires `plantuml <http://plantuml.com/>`_. Everything except `plantuml` is on pypi so you can get them with pip::

   pip install sphinx
   pip install sphinxcontrib-plantuml
   pip install alabaster

If you are using ubuntu you can use ``apt-get`` to get `plantuml`::

   apt-get install plantuml

Once everything is installed you can build the documentation using the Makefile. To build the html, for example::

   make html

This should create a folder named ``doc`` with an ``html`` sub-folder containing the documentation.

.. note:: If this is installed in a `virtualenv` then both the `sphinx` installation and the `theape` installation have to be in the same `virtualenv` or the auto-summaries for the code won't be built.

Installing Testing Dependencies
-------------------------------

The APE is currently being tested using `behave <http://pythonhosted.org/behave/>`_ so if you want to run the tests, you'll need that, `pyhamcrest <http://pyhamcrest.readthedocs.org/en/1.8.0/>`_ and `mock <http://mock.readthedocs.org/en/latest/magicmock.html>`_. All three are on pypi so if you have pip installed you can install them from the web (if installing system wide run as root).

.. code:: bash

   pip install behave
   pip install pyhamcrest
   pip install mock

