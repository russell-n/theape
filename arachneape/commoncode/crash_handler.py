
# this package
from arachneape.commoncode.strings import RED, BOLD, RESET


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
            red_error = "{red}{bold}{{error}}{reset}".format(red=RED,
                                                             bold=BOLD,
                                                             reset=RESET)
            crash_notice = "{bold}********** {msg} **********{reset}".format(red=RED,
                                                                msg=self.error_message,
                                                                             bold=BOLD,
                                                                             reset=RESET)
            self.logger.error(crash_notice)
            
            import traceback
            import sys
            import os
            
            exc_type, exc_value, exc_tb = sys.exc_info()
            tb_info = traceback.extract_tb(exc_tb)
            filename, linenum, funcname, source = tb_info[-1]
            
            self.logger.error(red_error.format(error=error))
            self.logger.error(red_error.format(error="Failed Line: {0}".format(source)))
            self.logger.error(red_error.format(error="In Function: {0}".format(funcname)))
            self.logger.error(red_error.format(error="In File: {0}".format(os.path.basename(filename))))
            self.logger.error(red_error.format(error="At Line: {0}".format(linenum)))
            self.logger.debug(traceback.format_exc())
    return wrapped
