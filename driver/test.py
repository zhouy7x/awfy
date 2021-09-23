import os
import types
slave_hostname = "test@jstc-8700k.sh.intel.com"
cmd2 = 'ssh ' + slave_hostname
print(cmd2)
print cmd2[:-1]
# os.popen(cmd2)
print types.StringTypes