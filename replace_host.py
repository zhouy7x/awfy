#!/usr/bin/python
import os
from sys import argv

try:
    new_host = 'has_key'
    old_host = argv[2] if argv[2:] else 'has_'
    # if not old_host.endswith('.sh.intel.com'):
    #     old_host += '.sh.intel.com'
    # if not new_host.endswith('.sh.intel.com'):
    #     new_host += '.sh.intel.com'
except Exception as e:
    print "Error: Must give 2 params, old host and new host."
else:
    cmd = "grep -nr '%s' ." % old_host
    data = os.popen(cmd).readlines()
    # with open('host-log.txt') as f:
    #     data = f.readlines()
    path_list = map(lambda x: x[:x.find(':')], data)
    path_list = list(set(path_list))
    # print path_list, len(path_list)

    # replace old host to new host.
    for path in path_list:
        cmd = 'perl -pi -e "s/%s/%s/g" %s' % (old_host, new_host, path)
        print cmd
        os.system(cmd)

    # remove *.pyc
    # cmd = 'find / -name "*.pyc" -print | xargs rm'
    # os.system(cmd)
