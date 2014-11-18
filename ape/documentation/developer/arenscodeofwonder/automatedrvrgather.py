
# arenscode
import AutomationSuite.AutomatedRVRgather

# the ape
from ape.commoncode.code_graphs import module_diagram, class_diagram


module = str(AutomationSuite.AutomatedRVRgather.__file__).rstrip('c')
name = module_diagram(module=module, project='automatedrvrgather')
print ".. image:: {0}".format(name)


name = class_diagram('GatherTest', module)
print ".. image:: " + name
