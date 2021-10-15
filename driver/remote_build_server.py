# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import subprocess
import time
from optparse import OptionParser
from sys import argv
import utils

parser = OptionParser(usage="usage: %prog [options]")
parser.add_option("-d", "--device-type", dest="device_type", type="string", default="win64",
                  help="Device type (default: win64)")
parser.add_option("-m", "--mode", dest="mode_name", type="string", default=None, help="Config mode name")
parser.add_option("-i", "--is-debug", dest="is_debug", type="choice", choices=['false', 'true'], default='false', help="Debug mode")
parser.add_option("-c", "--config", dest="debug_config_path", type="string", default="client/tmp/config.json", help="Debug config path")
(options, progargs) = parser.parse_args()
print (options, progargs)


def kill_processes(device_type=options.device_type,
                   mode_name=options.mode_name,
                   is_debug=options.is_debug,
                   debug_config_path=options.debug_config_path):
    utils.InitConfig(device_type=device_type, mode_name=mode_name, is_debug=is_debug,
                     debug_config_path=debug_config_path)
    port = utils.config_get_default('main', 'port', 8799)
    build_host = utils.config_get_default('build', 'hostname')
    target_os = utils.config_get_default('main', 'target_os', 'linux')

    if target_os == 'win64':
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
    elif target_os == 'linux':
        try:
            ssh_port = int(utils.config_get_default('build', 'ssh_port', 22))
        except:
            raise Exception("could not get ssh port!")
        else:
            find_port_process = 'ssh ' + build_host
            if ssh_port != 22:
                find_port_process += ' -p ' + str(ssh_port)
            find_port_process += ' -- lsof -i :' + str(port)
            print find_port_process
            ret = os.popen(find_port_process).readlines()
            pids = []
            for tmp in ret:
                if tmp:
                    pid = tmp.split()[1]
                    if pid.isdigit():
                        pids.append(pid)
            print pids
            for pid in pids:
                kill_process = 'ssh ' + build_host
                if ssh_port != 22:
                    kill_process += ' -p ' + str(ssh_port)
                kill_process += ' -- kill -9 ' + str(pid)
                print kill_process
                os.system(kill_process)


if __name__ == '__main__':
    utils.InitConfig(device_type=options.device_type, mode_name=options.mode_name, is_debug=options.is_debug,
                     debug_config_path=options.debug_config_path)
    port = utils.config_get_default('main', 'port', 8799)
    build_driver = utils.config_get_default('build', 'driver', None)
    build_host = utils.config_get_default('build', 'hostname')
    name = utils.config_get_default('build', 'name', 'build-server')
    try:
        ssh_port = int(utils.config_get_default('build', 'ssh_port', 22))
    except:
        raise Exception("could not get ssh port!")
    else:
        try:
            cmd = ['ssh', build_host]
            if ssh_port != 22:
                cmd.append('-p')
                cmd.append(str(ssh_port))
            cmd += ['--', 'cd', build_driver, ';', 'python', 'build_server.py', str(port)]
            print ' '.join(cmd)
            # os.system(cmd)
            delayed = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            subprocess.Popen(['sed', '-e', 's/^/' + name + ': /'], stdin=delayed.stdout)
            output, retval = delayed.communicate()
            time.sleep(5)
        except:
            kill_processes()
