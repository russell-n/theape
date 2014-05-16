
# python standard library
import subprocess

# third party
import docopt

# this documentation
from commons import catch_exit
from commons import usage


print subprocess.check_output('ape run -h'.split())


print usage


run_args =  docopt.docopt(doc=usage, argv="run".split())
print run_args


run_usage = """`run` sub-command

Usage: ape run -h
       ape run [<configuration>...]

Positional Arguments:

    <configuration>   0 or more configuration-file names [default: ape.ini]

Options;

    -h, --help  This help message.

"""
print catch_exit(run_usage, argv=['-h'])


print docopt.docopt(doc=run_usage, argv=['run'])


print docopt.docopt(doc=run_usage, argv="run ape.ini man.ini".split())


catch_exit(usage, argv="run -h".split())


output = docopt.docopt(doc=usage, argv="run -h".split(),
                       options_first=True)
print output


if output['<command>'] == 'run':
    arguments = ['run'] + output['<argument>']
    catch_exit(run_usage, argv=arguments)


# pretend we imported this
MESSAGE = "running '{config}'"
def run(configurations):
    # empty lists evaluate to False
    if not configurations:
        configurations = ['ape.ini']    
    for configuration in configurations:
        print MESSAGE.format(config=configuration)
    return


output = docopt.docopt(doc=usage, argv='run cow.ini pie.ini'.split())
run(output['<argument>'])
