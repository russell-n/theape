
# third-party
from configobj import ConfigObj
from validate import Validator


configuration = """
[APE]
defined = a b
repetitions = 12
repetitions_list = 12, 23
operation_1 = plugin1, plugin2
operation_2 = plugin3
""".splitlines()

spec = """
[APE]
defined = string_list
repetitions = integer
repetitions_list = int_list(min=1)
__many__ = string_list
""".splitlines()

config_spec = ConfigObj(spec)
config = ConfigObj(configuration,
                   configspec=config_spec,
                   list_values=False,
                   _inspec=True)

validator = Validator()
config.validate(validator)

for key, value in config['APE'].iteritems():
    print "{0}: ({1}) {2}".format(key, type(value), value)
