Fetch Subcommand
----------------

The `fetch` sub-command should be similar to the `run` sub-command.

::

    # python standard library
    import subprocess
    
    # third-party
    import docopt
    
    # this documentation
    from commons import catch_exit, usage
    
    

::

    print subprocess.check_output('ape fetch -h'.split())
    
    

::

    usage: ape.interface fetch [-h] [--modules [MODULES [MODULES ...]]]
                               [names [names ...]]
    
    positional arguments:
      names                 List of plugin-names (default=['Ape'])
    
    optional arguments:
      -h, --help            show this help message and exit
      --modules [MODULES [MODULES ...]]
                            Non-ape modules
    
    
    

::

    fetch_usage = """fetch subcommand
        
    usage: ape fetch -h
           ape fetch [<name>...]  [--module <module> ...] 
    
    positional arguments:
        <name>                                List of plugin-names (default=['Ape'])
    
    optional arguments:
        -h, --help                           Show this help message and exit
        -m, --module <module> ...      Non-ape modules
    """
    catch_exit(fetch_usage, ['--help'])
    

::

    fetch subcommand
        
    usage: ape fetch -h
           ape fetch [<name>...]  [--module <module> ...] 
    
    positional arguments:
        <name>                                List of plugin-names (default=['Ape'])
    
    optional arguments:
        -h, --help                           Show this help message and exit
        -m, --module <module> ...      Non-ape modules
    



So it kind of looks like it works. I'm not sure if the `help` options should be optional or not, since all the arguments are optional. I guess it's a matter of taste.

::

    arguments = "fetch Dummy Sparky Iperf --module pig.thing --m cow.dog".split()
    output = docopt.docopt(doc=usage, argv=arguments, options_first=True)
    
    arguments = [output['<command>']] + output['<argument>']
    print docopt.docopt(doc=fetch_usage, argv=arguments)
    

::

    {'--help': False,
     '--module': ['pig.thing', 'cow.dog'],
     '<name>': ['Dummy', 'Sparky', 'Iperf'],
     'fetch': True}
    



.. warning:: the ``arguments = [output['<command>']] + output['<argument>']`` line in the above is necessary because the usage lines start with ``ape fetch`` but the ``fetch`` token is being assigned to the ``<command>`` key in the ``output`` dictionary so the ``<argument>`` list doesn't have it. If you don't re-add it to the arguments, `docopt` will print the usage string and quit. The `run` section above only worked because I cheated and assumed I was getting the list of file-names, not a list of arguments to pass to `docopt`.

.. note:: I mentioned it in the `run` section, but the first call to `docopt` has to set `options_first` to True or the options for the sub-command will get added to the top-level dictionary.
