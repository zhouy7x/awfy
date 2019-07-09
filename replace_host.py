#!/usr/bin/python
import os


host = raw_input('Please input your host name or ip(e.g. 10.239.44.86 or ssgs4-test.sh.intel.com): ')
if __name__ == '__main__':
    # grep -nr 'ssgs5-test.sh.intel.com' > host-log.txt
    with open('host-log.txt') as f:
        data = f.readlines()
    path_list = map(lambda x: x[:x.find(':')], data)
    # replace all host to localhost.
    for path in path_list:
        cmd = 'perl -pi -e "s/ssgs5-test.sh.intel.com/%s/g" %s' % (host, path)
        print cmd
        os.system(cmd)

    # remove *.pyc
    cmd = 'find / -name "*.pyc" -print | xargs rm'
    os.system(cmd)
