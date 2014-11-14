The Check Sub-Command
---------------------

::

    print subprocess.check_output('ape check -h'.split())
    

::

    usage: ape.interface.arguments check [-h] [--modules [MODULES [MODULES ...]]]
                                         [<config-file list> [<config-file list> ...]]
    
    positional arguments:
      <config-file list>    List of config files (e.g. *.ini -
                            default='['ape.ini']').
    
    optional arguments:
      -h, --help            show this help message and exit
      --modules [MODULES [MODULES ...]]
                            Space-separated list of non-ape modules with plugins
    
    

::

    from commons import check_usage
    catch_exit(check_usage, argv=['-h'])
    

::

    `check` sub-command
    
    usage: ape check -h
           ape check  [<config-file-name> ...] [--module <module> ...]
    
    Positional Arguments:
    
        <config-file-name> ...    List of config files (e.g. *.ini - default='['ape.ini']')
    
    optional arguments:
    
        -h, --help                  Show this help message and exit
        -m, --module <module>       Non-ape module with plugins
    

::

    arguments = "check --module cow.dog.man ape.ini -m pip.ini".split()
    output = docopt.docopt(doc=usage, argv=arguments, options_first=True)
    
    arguments = [output['<command>']] + output['<argument>']
    
    print docopt.docopt(doc=check_usage, argv=arguments)
    
    

::

    {'--help': False,
     '--module': ['cow.dog.man', 'pip.ini'],
     '<config-file-name>': ['ape.ini'],
     'check': True}
    
    



.. warning:: I originally used `<config-file name>` for the config files, but `docopt` couldn't properly parse it. It might be safer to leave whitespace out of the names, especially when mixing positional arguments and options.

.. '
