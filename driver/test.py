#!/usr/bin/python
import json
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
config_name = './client/jsc/hsw-nuc-jsc-x64.config'
# utils.InitConfig(config_name)

# port = utils.config_get_default('main', 'port', 8799)
# build_driver = utils.config_get_default('build', 'driver', None)
# build_host = utils.config_get_default('build', 'hostname')
# build_host = 'awfy@10.239.61.116'
#
# try:
#     time.sleep(5)
# except:
#     print 'hhhh'
#     find_port_process = 'ssh ' + build_host + ' "netstat -ano | findstr :' + str(port) + '"'
#     print find_port_process
#     ret = os.popen(find_port_process).readlines()
#     pids = []
#     for tmp in ret:
#         if tmp:
#             pid = tmp.split()[-1]
#             pids.append(pid)
#     print pids
#     for pid in pids:
#         kill_process = 'ssh ' + build_host + ' "taskkill.exe -f -pid ' + pid + '"'
#         print kill_process
#         os.system(kill_process)


def to_dict(config_name):
    with open(config_name) as f:
        data = f.read()
    reg_string = re.findall(r'(\[(\w+)\][^\[]+)', data)
    # print reg_string
    dict2 = {}
    for tmp in reg_string:
        # print tmp[1]
        lines = tmp[0].splitlines()
        dict1 = {}
        for line in lines:
            tmp2 = line.split(' = ')
            try:
                value = tmp2[1]
                key = tmp2[0]
            except Exception as e:
                continue

            if 'true' in value:
                value = True
            elif 'false' in value:
                value = False
            dict1[key] = value

        dict2[tmp[1]] = dict1
    return dict2


config_dict = {}
modes = os.listdir('client')
for mode_name in modes:
    if mode_name == 'tmp':
        continue
    elif mode_name == 'win64-v8' or mode_name == 'win64-chrome':
        device = 'win64'

    device_list = []
    file_names = os.listdir(os.path.join('client', mode_name))
    for file_name in file_names:
        config_name = os.path.join('client', mode_name, file_name)
        dict2 = to_dict(config_name)


        # device = 'jsc'
        dict2['name'] = file_name.split('.')[0]
        if 'long-time' not in file_name and 'x86' not in file_name and 'patch' not in file_name:
            if '3900' in file_name or '9900' in file_name:
                dict2['enable'] = True
        device_list.append(dict2)
        config_dict[device] = device_list



with open('config.json', 'w') as f:
    f.write(json.dumps(config_dict))
