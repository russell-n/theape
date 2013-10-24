
# this package
import ape.interface.arguments
from ape.log_setter import set_logger


def enable_debugging(args):
    """
    Enables interactive debugging

    :param:

     - `args`: A namespace with pudb and pdb attributes
    """
    if args.pudb:
        import pudb
        pudb.set_trace()
        return
    if args.pdb:
        import pdb
        pdb.set_trace()
    return


def main():
    argue = ape.interface.arguments.ArgumentClinic()
    args = argue()
    set_logger(args)
    enable_debugging(args)
    args.function(args)
    return
