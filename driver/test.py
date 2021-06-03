#!/usr/bin/python
import re
import os
import time

import utils

# utils.InitConfig('./client/win64-chrome/amd-3900x.config')
# print utils.RemoteBuild
#
# print utils.RemoteBuildRepoPath
#
#
# ConfigPort = '1a231'
# try:
#     BuildPort = int(ConfigPort)
# except ValueError as e:
#     print e
#     raise ValueError("port must be int, not " + ConfigPort)
config_name = './client/win64-chrome/intel-9900k.config'
utils.InitConfig(config_name)

port = utils.config_get_default('main', 'port', 8799)
build_driver = utils.config_get_default('build', 'driver', None)
build_host = utils.config_get_default('build', 'hostname')
build_host = 'awfy@10.239.61.116'

try:
    time.sleep(5)
except:
    print 'hhhh'
    find_port_process = 'ssh ' + build_host + ' "netstat -ano | findstr :' + str(port) + '"'
    print find_port_process
    ret = os.popen(find_port_process).readlines()
    pids = []
    for tmp in ret:
        if tmp:
            pid = tmp.split()[-1]
            pids.append(pid)
    print pids
    for pid in pids:
        kill_process = 'ssh ' + build_host + ' "taskkill.exe -f -pid ' + pid + '"'
        print kill_process
        os.system(kill_process)


