The List Sub-Command
--------------------

This lists the plugins, so it should be even simpler, I think.

::

    print subprocess.check_output('ape list -h'.split())
    
    

::

    usage: ape.interface list [-h] [--modules [MODULES [MODULES ...]]]
    
    optional arguments:
      -h, --help            show this help message and exit
      --modules [MODULES [MODULES ...]]
                            Space-separated list of non-ape modules with plugin
    s
    
    
    

::

    list_usage = """list subcommand
    
    usage: ape list -h
           ape list [<module> ...]
    
    Positional Arguments:
      <module> ...  Space-separated list of importable module with plugins
    
    optional arguments:
    
      -h, --help                 Show this help message and exit
    
    """
    catch_exit(list_usage, ['-h'])
    
    

::

    list subcommand
    
    usage: ape list -h
           ape list [<module> ...]
    
    Positional Arguments:
      <module> ...  Space-separated list of importable module with plugins
    
    optional arguments:
    
      -h, --help                 Show this help message and exit
    
    



.. note:: The ``--help`` overrides everything, so even though that last call was missing ``list`` as the first argv element, it still works.

::

    print docopt.docopt(list_usage, argv=['list'])
    
    

::

    {'--help': False,
     '<module>': [],
     'list': True}
    
    

::

    arguments = 'list man.dog bill.ted'.split()
    base_output = docopt.docopt(doc=usage, argv=arguments, options_first=True)
    
    arguments = [base_output['<command>']] + base_output['<argument>'] 
    print docopt.docopt(list_usage, argv=arguments)
    
    

::

    {'--help': False,
     '<module>': ['man.dog', 'bill.ted'],
     'list': True}
    
    



The inability to pass in a list to an option seems like a flaw. Either I can be consistent and require the '-m' option when adding modules or use a positional argument. Maybe '-m' would be better, since it would probably be a rare thing to use, and it would be better to be consistent, but I think since there's no other options I'll just leave it like this.
