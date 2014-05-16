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

    usage: ape.interface [-h] [--debug] [-v] [--silent] [--pudb] [--pdb] [--trace]
                         [--callgraph]
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