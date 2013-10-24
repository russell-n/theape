
BLUE = "\033[34m"
RED  = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0;0m"


NEWLINE = '\n'
# constants for formatting output
RED_THING =  "{red}{{{{thing}}}}{reset} {{verb}}".format(red=RED, reset=RESET)
BOLD_THING = "{bold}{{thing}}{reset} {{{{value}}}}".format(bold=BOLD, reset=RESET)
CALLED_ON = "'{blue}{{attribute}}{reset}' attribute called on {red}{{thing}}{reset}".format(blue=BLUE,
                                                                                             red=RED,
                                                                                             reset=RESET)

CREATION = RED_THING.format(verb='Created')
ARGS = BOLD_THING.format(thing='Args:')
KWARGS = BOLD_THING.format(thing='Kwargs:')
CALLED = RED_THING.format(verb='Called')
NOT_IMPLEMENTED = RED_THING.format(verb='Not Implemented')

