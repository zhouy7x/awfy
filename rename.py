#!/usr/bin/python
import os
import re
from sys import argv

try:
    # old_host = argv[1]
    # new_host = argv[2]
    old_name = '--future'
    new_name = '-future'
except Exception as e:
    print "Error: Must give 2 params, old host and new host."
else:
    cmd = 'find . -name "*%s*"' % old_name
    data = os.popen(cmd).readlines()

    """
    ./driver/client/v8/hsw-nuc-x64--future-long-time.config
    """
    # for tmp in data:
    #     t = re.findall(r'(.*)('+old_name+')(.*)', tmp)[0]
    #     print t
    path_list = map(lambda x: re.findall(r'(.*)('+old_name+')(.*)', x)[0], data)
    # path_list = map(lambda x: x[:x.find(':')], data)
    path_list = list(set(path_list))
    # print path_list, len(path_list)

    # replace old host to new host.
    for name in path_list:
        cmd = 'mv '+''.join(name)+' '+name[0]+new_name+name[2]
        print cmd
        os.system(cmd)

    # remove *.pyc
    # cmd = 'find / -name "*.pyc" -print | xargs rm'
    # os.system(cmd)
