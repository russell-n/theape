
# the ape
from ape import BaseClass
from ape.interface.arguments import BaseArguments
from ape.interface.arguments import FetchArguments
from ape.interface.arguments import RunArguments
from ape.interface.arguments import ListArguments
from ape.interface.arguments import CheckArguments
from ape.interface.arguments import HelpArguments


names = 'fetch run list check help'.split()
definitions = (FetchArguments, RunArguments, ListArguments,
               CheckArguments, HelpArguments)
argument_definitions = dict(zip(names, definitions))


class ArgumentBuilder(BaseClass):
    """
    An adapter so this can go where the ArgumentClinic was
    """
    def __init__(self, args=None):
        """
        ArgumentBuilder Constructor

        :param:

         - `args`: list of args to use instead of sys.argv
        """
        super(ArgumentBuilder, self).__init__()
        self.args = args
        return

    def __call__(self):
        """
        Fake parse-args

        :return: sub-argument (e.g. RunArguments) based on command in args
        """
        args = BaseArguments(args=self.args)
        try:
            return argument_definitions[args.command](args=self.args)
        except KeyError as error:
            self.logger.debug(error)
            self.logger.error("Unknown sub-command '{0}'".format(args.command))
            print args.usage
            sys.exit()
        return args
