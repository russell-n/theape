The Run Sub-Command
-------------------

Setting the options above by themselves doesn't really seem useful because the Ape expects sub-commands as well so we'll have to add them. First we'll tackle the `run` sub-command.

.. '

::

    print subprocess.check_output('ape run -h'.split())
    
    

::

    usage: ape.interface run [-h] [<config-file list> [<config-file list> ...]]
    
    
    positional arguments:
      <config-file list>  A list of config file name (default='['ape.ini']').
    
    optional arguments:
      -h, --help          show this help message and exit
    
    
    



This looks easy enough, but first we have to add a `<command>` argument to the base usage-string so that we'll know that the user wants to get the `run` sub-command. We'll also need a list of optional `<argument>` inputs to pass to the sub-command.

::

    APE
    Usage: ape -h | -v
           ape [--debug | --silent] [--pudb | --pdb] <command> [<argument>...]
           ape [--trace | --callgraph]
    
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
    
    
    
    

::

    run_args =  docopt.docopt(doc=usage, argv="run".split())
    print run_args
    
    

::

    {'--callgraph': False,
     '--debug': False,
     '--help': False,
     '--pdb': False,
     '--pudb': False,
     '--silent': False,
     '--trace': False,
     '--version': False,
     '<argument>': [],
     '<command>': 'run'}
    
    



On Variable Conventions
~~~~~~~~~~~~~~~~~~~~~~~

`docopt` allows you to name the variables (that hold the values users pass in to options and arguments) using either all uppercased letters (e.g. ``MODULES``) or by lower-cased letters surrounded by angle brackets (e.g. ``<modules>``). I looked at several commands on my machine and noticed the following:

   * `iperf` uses brackets (``-o <filename>``) unless it expects a number in which case it uses a pound sign (``-i #``)
   * `nmap` uses angle brackets (``--max-retries <tries>``)
   * `man` uses all caps and an equals sign (``-L=LOCALE``)
   * `ls` uses uppercase and `=` (``--sort=WORD``)
   * `ping` uses lower-cased variable names (``-i interval``)   
   * `argparse` (what the ape is using) uses UPPERCASE without an equal sign unless you set the `metavar` yourself in which case it uses angle brackets
      - ``--modules [MODULES [MODULES...]]``
      - ``<config-file list>``

The `ping` convention won't work with docopt, since it uses either brackets or upper-cased letters to decide what's a variable. I can't really decide which of the remaining conventions is better. I think the UPPERCASE convention makes them stand out more and angle brackets introduce extra visual noise, but using equals signs seems confusing, since you don't actually use them in the command (then again, you don't use ellipses and square brackets either (oh, well)). I was thinking about using the `argparse` default convention of using uppercased letters without an equals sign, but it occurred to me that using the angle brackets allows you to create arbitrary strings with punctuation and whitespace (``<config-file list>`` vs ``CONFIGFILELIST``) so I think I'll stick to the angle-brackets for now. (although see the :ref:`Check Sub-Command <docopt-reproducingape-check-sub-command>` section for a problem that I ran into)

Back to the Sub-Command
~~~~~~~~~~~~~~~~~~~~~~~

The kind of disappointing part of `docopt` is that we don't have a way to automatically pass things off to the sub-command. Instead we have to create a new parser or interpret the running ourselves. 

.. '

::

    run_usage = """`run` sub-command
    
    Usage: ape run -h
           ape run [<configuration>...]
    
    Positional Arguments:
    
        <configuration>   0 or more configuration-file names [default: ape.ini]
    
    
    Options;
    
        -h, --help  This help message.
    
    """
    print catch_exit(run_usage, argv=['-h'])
    
    

::

    `run` sub-command
    
    Usage: ape run -h
           ape run [<configuration>...]
    
    Positional Arguments:
    
        <configuration>   0 or more configuration-file names [default: ape.ini]
    
    
    Options;
    
        -h, --help  This help message.
    
    
    

::

    print docopt.docopt(doc=run_usage, argv=['run'])
    
    

::

    {'--help': False,
     '<configuration>': [],
     'run': True}
    
    



It looks like it doesn't allow you to set a default for positional arguments, so you'd have to check yourself or change the positional argument to an option. Let's make sure that the <config> arguments are working at least.

.. '

::

    print docopt.docopt(doc=run_usage, argv="run ape.ini man.ini".split())
    
    

::

    {'--help': False,
     '<configuration>': ['ape.ini', 'man.ini'],
     'run': True}
    
    



Okay, but the idea for using this is that the `run` help would be reached from the base ape configuration. How does that work?

::

    catch_exit(usage, argv="run -h".split())
    
    

::

    APE
    Usage: ape -h | -v
           ape [--debug | --silent] [--pudb | --pdb] <command> [<argument>...]
           ape [--trace | --callgraph]
    
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
    
    



Okay, so that wasn't what I wanted -- the ``-h`` got caught before the sub-command was set and the top-level help got dumped to the screen. It turns out that there's a docopt parameter called ``options_first`` which is False by default. When it's True, the top-level options are only intrepreted before you get to the first positional argument and then rest are passed to the argument. So this would get the ape's help and ignore everything else::

    ape -h run

While this would pass the -h in as an argument for the ``<command>`` entry in the returned dictionary.

::

    output = docopt.docopt(doc=usage, argv="run -h".split(),
                           options_first=True)
    print output
    
    

::

    {'--callgraph': False,
     '--debug': False,
     '--help': False,
     '--pdb': False,
     '--pudb': False,
     '--silent': False,
     '--trace': False,
     '--version': False,
     '<argument>': ['-h'],
     '<command>': 'run'}
    
    



So now to make it work we would need to check the ``<command>`` entry and pass the arguments to docopt using the run-usage string instead.

::

    if output['<command>'] == 'run':
        arguments = ['run'] + output['<argument>']
        catch_exit(run_usage, argv=arguments)
    
    

::

    `run` sub-command
    
    Usage: ape run -h
           ape run [<configuration>...]
    
    Positional Arguments:
    
        <configuration>   0 or more configuration-file names [default: ape.ini]
    
    
    Options;
    
        -h, --help  This help message.
    
    



.. note:: This fixes the inability to pass in the `help` option to the sub-command, but the behavior is now different from ArgParse -- ArgParse keeps all the arguments at the top level (e.g. if `args` is the argparse namespace object, `args.configuration` would have the list of configuration files) but now the arguments specific to the sub-command are kept in a list (``output['<argument>']``) and need to be re-parsed using the sub-command's usage string and docopt.

.. '

Presumably the `run_usage` string would be imported from the module where the `run` function is (the `docopt` documentation says that the intention is for the usage-string to be in the module's docstring (``__doc__``)).

.. '

Now we should check the case where the user passed in some configuration file names. Although we would normally have to check for the command, I'll just assume it's working correctly here to save space.

::

    # pretend we imported this
    MESSAGE = "running '{config}'"
    def run(configurations):
        # empty lists evaluate to False
        if not configurations:
            configurations = ['ape.ini']    
        for configuration in configurations:
            print MESSAGE.format(config=configuration)
        return
    
    

::

    output = docopt.docopt(doc=usage, argv='run cow.ini pie.ini'.split())
    run(output['<argument>'])
    
    

::

    running 'cow.ini'
    running 'pie.ini'
    
    

