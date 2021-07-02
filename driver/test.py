#!/usr/bin/python
import json
import re
import os
import time

# import utils

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
    reg_string = re.findall(r'(\[([\w-]+)\][^\[]+)', data)
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
types = os.listdir('client')
for type_name in types:
    device_type = None
    if type_name == 'tmp':
        continue
    # elif mode_name == 'win64-v8' or mode_name == 'win64-chrome':
    #     device = 'win64'
    # elif mode_name == 'jsc':
    #     device = 'jsc'

    file_names = os.listdir(os.path.join('client', type_name))
    for file_name in file_names:
        device_list = []
        config_name = os.path.join('client', type_name, file_name)
        json_dict = to_dict(config_name)

        if ('8700k' in file_name or '3800x' in file_name) and 'x86' not in file_name and 'long-time' not in file_name \
                and 'patch' not in file_name:
            device_type = 'x64'
        elif 'a53' in file_name:
            device_type = 'arm'
        elif 'hsw-nuc-jsc-x64' in file_name and 'long-time' not in file_name and type_name == 'jsc':
            device_type = 'jsc'
        elif ('9900k' in file_name or '3900x' in file_name) and 'x86' not in file_name \
                and 'long-time' not in file_name and 'patch' not in file_name:
            device_type = 'win64'
        elif ('apl' in file_name or 'arm' in file_name) and 'x86' not in file_name and 'long-time' not in file_name \
                and 'patch' not in file_name and type_name == 'v8':
            device_type = 'v8'
        else:
            continue
        # saved device type
        if device_type in config_dict and device_type is not None:
            device_list = config_dict[device_type]
        # get mode name
        mode_name = ''
        if 'v8' in type_name:
            mode_name += 'v8'
        elif 'chrome' in type_name:
            mode_name += 'chrome'
        elif 'jsc' in type_name:
            mode_name += 'jsc'

        if mode_name:
            mode_name += '-'
        mode_name += file_name.split('.')[0]
        json_dict['name'] = mode_name

        # if 'long-time' not in file_name and 'x86' not in file_name and 'patch' not in file_name:
        #     if '3900' in file_name or '9900' in file_name:
        #         dict2['enable'] = True
        device_list.append(json_dict)
        config_dict[device_type] = device_list


with open('config.json', 'w') as f:
    f.write(json.dumps(config_dict))

import utils
utils.InitConfig('win64', 'v8-amd-3900x-x64')

