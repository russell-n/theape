
# python standard library
import re
import random
import string
# third-party
from behave import given, when, then
from hamcrest import assert_that, is_, \
     equal_to, is_not, close_to
from configobj import ConfigObj

# this package
from theape.parts.iperf.iperfsettings import iperf_configspec,\
     IperfConstants, get_validator

configspec = iperf_configspec.splitlines()
validator = get_validator()
BYTES_ONLY = 'bBkKmM '
INTEGER_UNITS = "{0}{1}"
REPORTS = 'cdmsvCDMSV'

@given("a configspec with a valid format option")
def valid_format(context):
    context.expected = random.choice('aAbBkKmMgG')
    source = ['format = {0}'.format(context.expected)]
    context.option = 'format'
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@when("the configspec is validated")
def validate(context):
    context.valid = context.configobj.validate(validator)
    try:
        context.value = context.configobj[context.option]
    except KeyError:
        context.value = None
    return

@then("the configspec outcome is as expected")
def assert_outcome(context):
    assert_that(context.value,
                is_(equal_to(context.expected)),
                'actual: {0} != expected: {1}'.format(context.value,
                                        context.expected))
    assert_that(context.valid,
                is_(True),
                '{0} did not validate'.format(context.configobj))
    return

@given("a configspec with a invalid format option")
def invalid_format(context):
    context.expected = random.choice('q t o l'.split())
    source = ['format = {0}'.format(context.expected)]
    context.option = 'format'
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@then("the configspec outcome is False")
def assert_false(context):
    assert_that(context.value,
                is_(equal_to(context.expected)),
                'actual: {0} != expected: {1}'.\
                format(context.value,
                       context.expected))
    assert_that(context.valid,
                is_not(True),
                '{0} validated'.format(context.configobj))
    return

@given("a configspec with a missing format option")
def missing_format(context):
    source = ['option=value']
    context.option = 'format'
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@then("the configspec outcome is None")
def assert_none(context):
    assert_that(context.value,
                is_(None),
                '{0} is not None'.format(context.value))
    return

@given("a configspec with a valid interval option")
def valid_interval(context):
    context.expected = random.uniform(0, 100)
    context.option = 'interval'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@then('the configspec outcome is positive float')
def assert_float(context):
    assert_that(context.value,
                is_(close_to(context.expected,
                             0.001)),
                'actual: {0} != {1}'.format(context.value,
                    context.expected))
    return

@given("a configspec with a invalid interval option")
def valid_interval(context):
    # invalid numbers are still gathered
    # they are just left as strings
    context.actual = random.randrange(0, -100, -1)
    context.expected = str(context.actual)
    context.option = 'interval'
    source = ['{1} = {0}'.format(context.actual,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a missing interval option")
def missing_interval(context):    
    source = ['option=value']
    context.option = 'interval'
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid len option")
def valid_len(context):
    context.value = random.randrange(0, 100)
    suffix = random.choice(' BKMG')
    context.expected = INTEGER_UNITS.format(context.value,
                                       suffix.strip())
    context.option = 'len'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a invalid len option")
def invalid_len(context):
    context.actual = random.randrange(-1, -100, -1)
    context.expected = str(context.actual)
    context.option = 'len'
    source = ['{1} = {0}'.format(context.actual,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a missing len option")
def missing_interval(context):    
    source = ['option=value']
    context.option = 'len'
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid print_mss option")
def valid_len(context):
    context.expected = True
    context.option = 'print_mss'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@then('the configspec outcome is True')
def assert_true(context):
    assert_that(context.value,
                is_(True),
                "'{0}' is not True".format(context.value))
    assert_that(context.valid,
                is_(True),
                "'{0}' did not validate".format(context.configobj))
    return

@given("a configspec with a invalid print_mss option")
def invalid_print_mss(context):
    context.actual = 'aoeusnth'
    context.expected = context.actual
    context.option = 'len'
    source = ['{1} = {0}'.format(context.actual,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a missing print_mss option")
def missing_print_mss(context):    
    source = ['option=value']
    context.option = 'print_mss'
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid output option")
def valid_len(context):
    context.expected = 'aoeunsthc.iperf'
    context.option = 'output'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a missing output option")
def missing_print_mss(context):    
    source = ['option=value']
    context.option = 'output'
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid port option")
def valid_port(context):
    context.expected = random.randrange(1024, 65536)
    context.option = 'port'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a invalid port option")
def invalid_print_mss(context):
    context.actual = random.randrange(-100, 1024)    
    context.expected = str(context.actual)
    context.option = 'port'
    source = ['{1} = {0}'.format(context.actual,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid udp option")
def valid_port(context):
    context.expected = True
    context.option = 'udp'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid window option")
def valid_port(context):
    prefix = random.randrange(0, 100)
    suffix = random.choice(BYTES_ONLY)    
    context.expected = INTEGER_UNITS.format(prefix,
                                       suffix.strip())
    context.option = 'window'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a invalid window option")
def invalid_window(context):
    prefix = random.randrange(0, 100)
    suffix = random.choice('gzGq')    
    context.expected = INTEGER_UNITS.format(prefix,
                                       suffix)
    context.option = 'window'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid bind option")
def valid_bind(context):
    context.expected = "aoentuh"
    context.option = 'bind'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a missing bind option")
def missing_print_mss(context):    
    source = ['option=value']
    context.option = 'bind'
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid compatibility option")
def valid_bind(context):
    context.expected = True
    context.option = 'compatibility'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid mss option")
def valid_bind(context):
    prefix = random.randrange(100)
    suffix = random.choice(BYTES_ONLY)
    context.expected = INTEGER_UNITS.format(prefix,
                                            suffix.strip())
    context.option = 'mss'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a invalid mss option")
def invalid_window(context):
    prefix = random.randrange(0, 100)
    suffix = random.choice('gzGq')    
    context.expected = INTEGER_UNITS.format(prefix,
                                       suffix)
    context.option = 'mss'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid nodelay option")
def valid_bind(context):
    context.expected = True
    context.option = 'nodelay'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid IPv6Version option")
def valid_bind(context):
    context.expected = True
    context.option = 'IPv6Version'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid single_udp option")
def valid_single_udp(context):
    context.expected = True
    context.option = 'single_udp'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid daemon option")
def valid_daemon(context):
    context.expected = True
    context.option = 'daemon'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid bandwidth option")
def valid_bandwidth(context):
    prefix = random.randrange(100, 1000)
    suffix = random.choice('kmKM')
    context.expected = INTEGER_UNITS.format(prefix, suffix)
    context.option = 'bandwidth'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a invalid bandwidth option")
def invalid_window(context):
    prefix = random.randrange(0, 100)
    suffix = random.choice('sw ')    
    context.expected = INTEGER_UNITS.format(prefix,
                                       suffix.strip())
    context.option = 'bandwidth'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid dualtest option")
def valid_dualtest(context):
    context.expected = True
    context.option = 'dualtest'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid num option")
def valid_bandwidth(context):
    prefix = random.randrange(100, 1000)
    suffix = random.choice('bBkmKMgG')
    context.expected = INTEGER_UNITS.format(prefix, suffix)
    context.option = 'num'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a invalid num option")
def invalid_window(context):
    prefix = random.randrange(0, 100)
    suffix = random.choice('sw')    
    context.expected = INTEGER_UNITS.format(prefix,
                                       suffix.strip())
    context.option = 'num'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid tradeoff option")
def valid_bandwidth(context):
    context.expected = True
    context.option = 'tradeoff'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid time option")
def valid_bandwidth(context):
    context.expected = random.randrange(100)
    context.option = 'time'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a invalid time option")
def invalid_time(context):
    context.expected = str(random.randrange(-1, -111, -1))

    context.option = 'time'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid fileinput option")
def valid_fileinput(context):
    context.expected = 'environment.py'
    context.option = 'fileinput'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a missing fileinput option")
def missing_fileinput(context):    
    source = ['option=value']
    context.option = 'fileinput'
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a invalid fileinput option")
def invalid_fileinput(context):
    context.expected = 'aoeusnthc.wdes'

    context.option = 'fileinput'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid listenport option")
def valid_fileinput(context):
    context.expected = random.randrange(1024, 4000)
    context.option = 'listenport'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a invalid listenport option")
def invalid_fileinput(context):
    context.expected = str(random.randrange(1024))
    context.option = 'listenport'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid parallel option")
def valid_parallel(context):
    context.expected = random.randrange(1, 4000)
    context.option = 'parallel'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a invalid parallel option")
def invalid_fileinput(context):
    context.expected = str(random.randrange(0, -100, -1))
    context.option = 'parallel'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid ttl option")
def valid_ttl(context):
    context.expected = random.randrange(-1, 4000)
    context.option = 'ttl'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid linux-congestion option")
def valid_linux_congestion(context):
    context.expected = "cubit"
    context.option = 'linux-congestion'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid reportexclude option")
def valid_reportexclude(context):
    context.expected = random.choice(REPORTS)
    context.option = 'reportexclude'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a invalid reportexclude option")
def invalid_fileinput(context):
    choices = [letter for letter in string.letters if \
               letter not in REPORTS]
    context.expected = random.choice(choices)
    context.option = 'reportexclude'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a valid reportstyle option")
def valid_reportexclude(context):
    context.expected = random.choice('cC')
    context.option = 'reportstyle'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return

@given("a configspec with a invalid reportstyle option")
def invalid_fileinput(context):
    context.expected = random.choice('4DLevt')
    context.option = 'reportstyle'
    source = ['{1} = {0}'.format(context.expected,
                                 context.option)]
    context.configobj = ConfigObj(source, configspec=configspec)
    return