The ArachneApe Plugin
=====================

This is a default plugin to provide the base-level of features. This allows the code to have a fall-back when the user does not specify a plugin. The use of the word `plugin` in the module name seems redundant, but I am trying to avoid namespace problems since the base package is named ``arachneape``.



.. uml::

   ArachneApe -|> BasePlugin
   ArachneApe o- HelpPage
   ArachneApe o- TheHortator

.. autosummary::
   :toctree: api

   ArachneApe
   ArachneApe.help
   ArachneApe.product
   ArachneApe.config



The Help
--------

To print the help-message the ArachneApe will use the help page, but since it is the default plugin it needs to construct things like the arguments and such. To keep it dynamic I am going to try and use the ArgumentParser instance. Here are the experiments.

.. currentmodule:: argparse
.. autosummary::
   
   argparse.ArgumentParser.format_usage

::

    if output_documentation:
        arguments = ArgumentClinic()
        arguments.add_arguments()
        arguments.add_subparsers()
        parser = arguments.parser
        print parser.format_usage()
    

::

    usage: arachneape.interface [-h] [--debug] [--silent] [--pudb] [--pdb]
                                {run,fetch,list,check,help} ...
    
    



Well, that might be kind of useful, although the program name is wrong and it does not show the sub-parser arguments.

::

    if output_documentation:
        parser.prog = 'arachneape'
        print parser.format_help()
    

::

    usage: arachneape [-h] [--debug] [--silent] [--pudb] [--pdb]
                      {run,fetch,list,check,help} ...
    
    optional arguments:
      -h, --help            show this help message and exit
      --debug               Sets the logging level to debug
      --silent              Sets the logging level to off (for stdout)
      --pudb                Enables the pudb debugger
      --pdb                 Enables the pdb debugger
    
    Sub-Commands Help:
      Available Subcommands
    
      {run,fetch,list,check,help}
                            SubCommands
        run                 Run the ArachneApe
        fetch               Fetch a sample config file.
        list                List available plugins.
        check               Check your setup.
        help                Show more help
    
    



Not really... most of the arguments actually go to the sub-commands but they are not shown.

After stepping through the code it looks like this is going to be more effort than it is worth, the sub-parsers are themselves instances of ArgumentParser and that simple help message being printed is going through quite a bit of code to get built up. I think I will just write it out for now.

Another Way
~~~~~~~~~~~

After taking a break I decided to just add the sub-commands to the ArgumentClinic as properties, that way I can try to query them directly.

.. currentmodule:: arachneape.interface.arguments
.. autosummary::
   :toctree: api

   ArgumentClinic

::

    if output_documentation:
        subs = (arguments.runner, arguments.fetcher,
                arguments.lister, arguments.checker, arguments.helper)
    
        program = 'arachneape[.\w]*'
        expression = re.compile(program)
        for sub in subs:
            print expression.sub('arachneape', sub.format_usage().replace('usage: ', ''))
    

::

    arachneape run [-h]
                                    [<config-file list> [<config-file list> ...]]
    
    arachneape fetch [-h] [names [names ...]]
    
    arachneape list [-h]
    
    arachneape check [-h]
                                      
                                      [<config-file list> [<config-file list> ...]]
    
    arachneape help [-h] [-w WIDTH] [name]
    
    



The regular-expression substitution is to get rid of the extra package name while still keeping the sub-command, otherwise it says ``arachneape.interface``.
