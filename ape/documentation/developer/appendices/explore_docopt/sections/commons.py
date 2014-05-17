import docopt

def catch_exit(usage, argv, version=None):
    try:
        print docopt.docopt(doc=usage, argv=argv,
                            version=version)
    except SystemExit as error:
        return error

usage = """APE
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

"""
    
run_usage = """`run` sub-command

Usage: ape run -h
       ape run [<configuration>...]

Positional Arguments:

    <configuration>   0 or more configuration-file names [default: ape.ini]

Options;

    -h, --help  This help message.

"""

fetch_usage = """fetch subcommand
    
usage: ape fetch -h
       ape fetch [<name>...]  [--module <module> ...] 

positional arguments:
    <name>                                List of plugin-names (default=['Ape'])

optional arguments:
    -h, --help                           Show this help message and exit
    -m, --module <module> ...      Non-ape modules
"""

list_usage = """list subcommand

usage: ape list -h
       ape list [<module> ...]

Positional Arguments:
  <module> ...  Space-separated list of importable module with plugins

optional arguments:

  -h, --help                 Show this help message and exit

"""

check_usage = """`check` sub-command

usage: ape check -h
       ape check  [<config-file-name> ...] [--module <module> ...]

Positional Arguments:

    <config-file-name> ...    List of config files (e.g. *.ini - default='['ape.ini']')

optional arguments:

    -h, --help                  Show this help message and exit
    -m, --module <module>       Non-ape module with plugins

"""

help_usage = """`help` sub-command

usage: ape help -h
       ape help [-w WIDTH] [--module <module>...] [<name>]

positional arguments:
    <name>                  A specific plugin to inquire about [default: ape].

optional arguments:
    -h, --help            show this help message and exit
    -w , --width <width>  Number of characters to wide to format the page.
    -m, --module <module>     non-ape module with plugins
    
"""
