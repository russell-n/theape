
def try_except(func):
    """
    A decorator method to catch Exceptions

    :param:

     - `func`: A function to call
    """
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            import traceback
            log = BaseClass()
            log.logger.error(error)
            log.logger.debug(traceback.format_exc())
    return wrapped


class UbootKommandant(object):
    pass
