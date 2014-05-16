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
    
