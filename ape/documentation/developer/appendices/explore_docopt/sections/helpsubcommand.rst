The Help Sub-Command
--------------------

::

    print subprocess.check_output('ape help -h'.split())
    

::

    usage: ape.interface.arguments help [-h] [-w WIDTH]
                                        [--modules [MODULES [MODULES ...]]]
                                        [name]
    
    positional arguments:
      name                  A specific plugin to inquire about.
    
    optional arguments:
      -h, --help            show this help message and exit
      -w WIDTH, --width WIDTH
                            Number of characters to wide to format the page.
      --modules [MODULES [MODULES ...]]
                            Space-separated list of non-ape modules with plugins
    
    

::

    from commons import help_usage
    catch_exit(help_usage, ["--help"])
    

::

    `help` sub-command
    
    usage: ape help -h
           ape help [-w WIDTH] [--module <module>...] [<name>]
    
    positional arguments:
        <name>                  A specific plugin to inquire about [default: ape].
    
    optional arguments:
        -h, --help            show this help message and exit
        -w , --width <width>  Number of characters to wide to format the page.
        -m, --module <module>     non-ape module with plugins
        
    

::

    output = docopt.docopt(usage, argv="help bob -w 30 -m cow.pipe".split(), op
    tions_first=True)
    arguments = [output['<command>']] + output['<argument>']
    print docopt.docopt(help_usage, arguments)
    
    

::

    {'--help': False,
     '--module': ['cow.pipe'],
     '--width': '30',
     '<name>': 'bob',
     'help': True}
    
    

