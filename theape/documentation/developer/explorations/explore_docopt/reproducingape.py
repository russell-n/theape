
# python standard library
import subprocess

# third party
import docopt

# the ape
from ape.main import main

# this documentation
from commons import catch_exit
from baseusagestring import usage


print subprocess.check_output('ape -h'.split())



print subprocess.check_output('ape fetch -h'.split())


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


arguments = "fetch Dummy Sparky Iperf --module pig.thing --m cow.dog".split()
output = docopt.docopt(doc=usage, argv=arguments, options_first=True)

arguments = [output['<command>']] + output['<argument>']
print docopt.docopt(doc=fetch_usage, argv=arguments)


print subprocess.check_output('ape list -h'.split())


list_usage = """list subcommand

usage: ape list -h
       ape list [<module> ...]

Positional Arguments:
  <module> ...  Space-separated list of importable module with plugins

optional arguments:

  -h, --help                 Show this help message and exit

"""
catch_exit(list_usage, ['-h'])


print docopt.docopt(list_usage, argv=['list'])


arguments = 'list man.dog bill.ted'.split()
base_output = docopt.docopt(doc=usage, argv=arguments, options_first=True)

arguments = [base_output['<command>']] + base_output['<argument>'] 
print docopt.docopt(list_usage, argv=arguments)


print subprocess.check_output('ape check -h'.split())


check_usage = """`check` sub-command

usage: ape check -h
       ape check  [<config-file-name> ...] [--module <module> ...]

Positional Arguments:

    <config-file-name> ...    List of config files (e.g. *.ini - default='['ape.ini']')

optional arguments:

    -h, --help                  Show this help message and exit
    -m, --module <module>       Non-ape module with plugins

"""

catch_exit(check_usage, argv=['-h'])


arguments = "check --module cow.dog.man ape.ini -m pip.ini".split()
output = docopt.docopt(doc=usage, argv=arguments, options_first=True)

arguments = [output['<command>']] + output['<argument>']

print docopt.docopt(doc=check_usage, argv=arguments)


print subprocess.check_output('ape help -h'.split())


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

catch_exit(help_usage, ["--help"])


output = docopt.docopt(usage, argv="help bob -w 30 -m cow.pipe".split(), options_first=True)
arguments = [output['<command>']] + output['<argument>']
print docopt.docopt(help_usage, arguments)
