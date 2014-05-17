Reproducing the APE's Interface
===============================

.. '

Since one of the reason's for exploring `docopt` is to find a way to simplify the argument parsing in the Ape, I'll see if I can reproduce it here.

Contents:

    * :ref:`The Ape's Usage String <docopt-reproducingape-ape-usage-string>`
    * :ref:`The Base Usage String <docopt-reproducingape-base-usage-string>`
    * :ref:`Run Sub-Command <docopt-reproducingape-run-sub-command>`
    * :ref:`Fetch Sub-Command <docopt-reproducingape-fetch-sub-command>`
    * :ref:`List Sub-Command <docopt-reproducingape-list-sub-command>`
    * :ref:`Check Sub-Command <docopt-reproducingape-check-sub-command>`
    * :ref:`Help Sub-Command <docopt-reproducingape-help-sub-command>`
    * :ref:`All the Usage Pages <docopt-reproducingape-usage-pages>`

.. '



.. _docopt-reproducingape-ape-usage-string:

The Ape's Usage String
----------------------

.. '

.. currentmodule:: ape
.. autosummary::
   :toctree: api

   ape.main

::

    print subprocess.check_output('ape -h'.split())
    
    

::

    usage: ape.interface.arguments [-h] [--debug] [-v] [--silent] [--pudb] [--pdb]
                                   [--trace] [--callgraph]
                                   {run,fetch,list,check,help} ...
    
    optional arguments:
      -h, --help            show this help message and exit
      --debug               Sets the logging level to debug
      -v, --version         Display the version number and quit
      --silent              Sets the logging level to off (for stdout)
      --pudb                Enables the pudb debugger
      --pdb                 Enables the pdb debugger
      --trace               Turn on code-tracing
      --callgraph           Create call-graph
    
    Sub-Commands Help:
      Available Subcommands
    
      {run,fetch,list,check,help}
                            SubCommands
        run                 Run the Ape
        fetch               Fetch a sample config file.
        list                List available plugins.
        check               Check your setup.
        help                Show more help
    
    


.. _docopt-reproducingape-base-usage-string:

.. include:: sections/baseusagestring.rst

.. _docopt-reproducingape-run-sub-command:
    
.. include:: sections/runsubcommand.rst
    
.. _docopt-reproducingape-fetch-sub-command:

.. include:: sections/fetchsubcommand.rst

.. _docopt-reproducingape-list-sub-command:

.. include:: sections/listsubcommand.rst

.. _docopt-reproducingape-check-sub-command:

.. include:: sections/checksubcommand.rst

.. _docopt-reproducingape-help-sub-command:

.. include:: sections/helpsubcommand.rst

.. _docopt-reproducingape-usage-pages:

All Usage Pages
---------------

Since I refer to these while coding I thought I'd put them in one place.

.. '

APE Usage
~~~~~~~~~

::

    APE
    Usage: ape -h | -v
           ape [--debug|--silent] [--pudb|--pdb] <command> [<argument>...]
           ape [--debug|--silent] [--trace|--callgraph] <command> [<argument>..
    .]
    
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
    
    



Run Usage
~~~~~~~~~

::

    `run` sub-command
    
    Usage: ape run -h
           ape run [<configuration>...]
    
    Positional Arguments:
    
        <configuration>   0 or more configuration-file names [default: ape.ini]
    
    
    Options;
    
        -h, --help  This help message.
    
    



Fetch Usage
~~~~~~~~~~~

::

    fetch subcommand
        
    usage: ape fetch -h
           ape fetch [<name>...]  [--module <module> ...] 
    
    positional arguments:
        <name>                                List of plugin-names (default=['A
    pe'])
    
    optional arguments:
        -h, --help                           Show this help message and exit
        -m, --module <module> ...      Non-ape modules
    
    



List Usage
~~~~~~~~~~

::

    list subcommand
    
    usage: ape list -h
           ape list [<module> ...]
    
    Positional Arguments:
      <module> ...  Space-separated list of importable module with plugins
    
    optional arguments:
    
      -h, --help                 Show this help message and exit
    
    



Check Usage
~~~~~~~~~~

::

    `check` sub-command
    
    usage: ape check -h
           ape check  [<config-file-name> ...] [--module <module> ...]
    
    Positional Arguments:
    
        <config-file-name> ...    List of config files (e.g. *.ini - default='[
    'ape.ini']')
    
    optional arguments:
    
        -h, --help                  Show this help message and exit
        -m, --module <module>       Non-ape module with plugins
    
    



Help Usage
~~~~~~~~~~

::

    `help` sub-command
    
    usage: ape help -h
           ape help [-w WIDTH] [--module <module>...] [<name>]
    
    positional arguments:
        <name>                  A specific plugin to inquire about [default: ap
    e].
    
    optional arguments:
        -h, --help            show this help message and exit
        -w , --width <width>  Number of characters to wide to format the page.
        -m, --module <module>     non-ape module with plugins
        
    
    

