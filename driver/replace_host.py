#!/usr/bin/python
import os
import re
from sys import argv

if __name__ == '__main__':
    file_name = "/change_path/host-log.txt"
    if argv[1:]:
        old_hostname = argv[1]
    else:
        old_hostname = 'ssgs2-test.sh.intel.com'

    # get old hostname's path.
    grep_cmd = "grep -nr %s /home/user/work/awfy > %s" % (old_hostname, file_name)
    os.system(grep_cmd)

    # get current service's hostname.
    hostname = os.popen('hostname').read()
    if re.match(r'^ssgs\d-test$', hostname):
        new_hostname = hostname.replace('\n', '') + ".sh.intel.com"
    else:
        new_hostname = hostname
    print new_hostname

    # replace hostname.
    if old_hostname != new_hostname:
        with open(file_name) as f:
            data = f.readlines()
        path_list = map(lambda x: x[:(x.find(':') if x.find(':') > 0 else 0)], data)
        # replace all host to localhost.
        for path in path_list:
            if path:
                cmd = 'perl -pi -e "s/%s/%s/g" %s' % (old_hostname, new_hostname, path)
                print cmd
                os.system(cmd)
    else:
        print "same hostnames!"
