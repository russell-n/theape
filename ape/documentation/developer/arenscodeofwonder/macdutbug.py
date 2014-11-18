
# python standard library
import shlex
import subprocess

# this package
from ape.commoncode.crash_handler import print_traceback


print subprocess.check_output(shlex.split('automationRunner -h'))


from configobj import ConfigObj
import AutomationSuite.AutomatedRVRgather as AutomatedRVRgather

config = ConfigObj('rvr.ini')

#test_object = AutomatedRVRgather.GatherTest(config['RvR'], False)
#test_object.RunTest()


from mock import MagicMock, patch
            

ssh_mock = MagicMock()
patcher = patch('paramiko.SSHClient')
ssh_connection = patcher.start()
try:
    test_object = AutomatedRVRgather.GatherTest(config['RvR'], False)
except NameError as error:
    print_traceback(error)
