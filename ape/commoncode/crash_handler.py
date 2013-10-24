
# this package
from ape.commoncode.strings import RED, BOLD, RESET


def try_except(method):
    """
    A decorator method to catch Exceptions

    :param:

     - `func`: A function to call
    """
    def wrapped(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except self.error as error:
            if hasattr(self, 'clean_up'):
                self.clean_up(error)
            else:
                log_error(error, self.logger, self.error_message)
    return wrapped


def log_error(error, logger, error_message):
    """
    Logs the error.
    """
    red_error = "{red}{bold}{{name}}: {reset}{red}{{msg}}{reset}".format(red=RED,
                                                                         bold=BOLD,
                                                                         reset=RESET)
    crash_notice = "{bold}********** {msg} **********{reset}".format(red=RED,
                                                                     msg=error_message,
                                                                     bold=BOLD,
                                                                     reset=RESET)
    logger.error(crash_notice)
            
    import traceback
    import sys
    import os
            
    exc_type, exc_value, exc_tb = sys.exc_info()
    tb_info = traceback.extract_tb(exc_tb)
    filename, linenum, funcname, source = tb_info[-1]

    error_message = red_error.format(name=error.__class__.__name__,
                                        msg=error)

    logger.error(error_message)
    logger.error(red_error.format(name="Failed Line",
                                               msg = source))
    logger.error(red_error.format(name="In Function",
                                               msg=funcname))
    logger.error(red_error.format(name="In File",
                                               msg=os.path.basename(filename)))
    logger.error(red_error.format(name="At Line",
                                               msg=linenum))
    logger.debug(traceback.format_exc())
    return
