
from configobj import ConfigObj, flatten_errors
from validate import Validator


configspec="""
[TEST]
value = LiteralString
""".splitlines()

config = """
[TEST]
value = NonLiteralString
""".splitlines()

config_spec = ConfigObj(configspec,
                        list_values=False,
                        _inspec=True)
configuration = ConfigObj(config, configspec=configspec)

validator = Validator()

outcome = configuration.validate(validator, preserve_errors=True)
print outcome


configspec="""
[TEST]
value = option('LiteralString')
""".splitlines()

config_spec = ConfigObj(configspec,
                        list_values=False,
                        _inspec=True)

configuration = ConfigObj(config, configspec=configspec)
outcome = configuration.validate(validator, preserve_errors=True)
print outcome


config = """
[TEST]
value = LiteralString
""".splitlines()

configuration = ConfigObj(config,
                          configspec=configspec)
outcome = configuration.validate(validator, preserve_errors=True)
print outcome


def process_errors(config, outcome):
    """
    Uses `flatten_errors` to find bad values

    :param:

      - `config`: ConfigObj that created the outcome
      - `outcome`: returned value from config.validate
    """
    if outcome:
        for section_list, key, error in flatten_errors(config, outcome):
            if key is not None:
                print key, section_list
                print "The '{0}' key in section '{1}' failed validation".format(key,
                                                                                ','.join(section_list))
            else:
                print "The '{0}' section was missing".format(','.join(section_list))
    return
    


config = """
[TEST]
value = BadValue
""".splitlines()

configuration = ConfigObj(config,
                          configspec=configspec)
outcome = configuration.validate(validator, preserve_errors=True)
process_errors(config, outcome)
