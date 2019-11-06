#!/usr/bin/python
import os
import re
import sys
import utils


def main():
    """
    1. get hostnames of all slaves;
    2. use expect auto run ssh-copy-id <hostname> ;
    :return:
    """
    # get hostnames
    hostnames = []
    config_dir = './client'
    modes = os.popen('ls %s' % config_dir).read().split()
    for mode in modes:
        folder = '%s/%s' % (config_dir, mode)
        files = os.popen('ls %s' % folder).read().split()
        for file in files:
            file_path = '%s/%s' % (folder, file)
            with open(file_path) as f:
                lines = f.readlines()
            for line in lines:
                ret = re.search(r'hostname ?= ?(.+)', line)
                if ret:
                    hostname = ret.group(1)
                    # print hostname
                    if hostname not in hostnames:
                        hostnames.append(hostname)
    # print hostnames

    # auto run ssh-copy-id <hostname>
    print "TODO: you must run next few commands one by one by yourself!!!"
    print "TODO: you must run next few commands one by one by yourself!!!"
    print "TODO: you must run next few commands one by one by yourself!!!"
    print ""
    for hostname in hostnames:
        print("ssh-copy-id " + hostname)


if __name__ == '__main__':
    with utils.chdir(sys.path[0]):
        print(">> Executing in " + os.getcwd())
        main()
