# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import subprocess
import time
from sys import argv
import utils


def kill_processes(config_name):
    utils.InitConfig(config_name)
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
    else:
        try:
            ssh_port = int(utils.config_get_default('build', 'ssh_port', 22))
        except:
            raise Exception("could not get ssh port!")
        else:
            find_port_process = 'ssh ' + build_host + ' "lsof -i :' + str(port)
            if ssh_port != 22:
                find_port_process += ' -p ' + str(ssh_port)
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
                kill_process = 'ssh ' + build_host + ' "kill -9 ' + str(pid)
                print kill_process
                os.system(kill_process)


if __name__ == '__main__':
    try:
        config_name = argv[1]
        utils.InitConfig(config_name)
    except Exception as e:
        print "Error: You must give a right config file path!!!"
        # raise Exception(e)
    else:
        port = utils.config_get_default('main', 'port', 8799)
        build_driver = utils.config_get_default('build', 'driver', None)
        build_host = utils.config_get_default('build', 'hostname')
        try:
            cmd = ['ssh', build_host, '--', 'cd', build_driver, ';', 'python', 'build_server.py', str(port)]
            print ' '.join(cmd)
            # os.system(cmd)
            delayed = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            subprocess.Popen(['sed', '-e', 's/^/' + 'win-server' + ': /'], stdin=delayed.stdout)
            output, retval = delayed.communicate()
            time.sleep(5)
            cmd = ['ssh', build_host, '--', 'powershell', '/c', 'cd', build_driver, ';', 'python', 'build_server.py', str(port)]
            print cmd
            # os.system(cmd)
            delayed = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            subprocess.Popen(['sed', '-e', 's/^/' + 'win-server' + ': /'], stdin=delayed.stdout)
            output, retval = delayed.communicate()
            time.sleep(5)
        except:
            kill_processes(config_name)
