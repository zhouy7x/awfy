#!/usr/bin/python
from sys import argv
import os
from devices_config import *


def kill_all(repos):
    """
    kill all progresses of awfy running scripts.
    :param repos:
    :return:
    """
    if not repos:
        print KILL_ERROR_MSG
        return
    elif repos == ['all']:
        repos = ALL_PROCESSES

    for param in repos:
        param = param.lower()
        if param not in ALL_PROCESSES:
            print KILL_ERROR_MSG
            return

        if param == 'apache2':
            cmd = '/etc/init.d/apache2 stop'
            if os.system(cmd):
                print('ERROR: stop apache2 error.')
            continue
        elif param == 'query':
            str_list = ["python query_server.py"]
        elif param in ['v8', '1800x']:
            str_list = [
                "python build_server_%s.py" % param,
                "bash schedule-run-%s.sh" % param,
                "python dostuff-%s.py" % param,
                "/home/user/depot_tools/ninja-linux64 -C /home/user/work/repos/chrome/%s" % param,
                "/home/user/depot_tools/ninja-linux64 -C /home/user/work/repos/v8/%s" % param,
                "Tools/Scripts/build-webkit --jsc-only",
            ]
        elif param in ['cyan', 'bigcore']:
            str_list = [
                "bash schedule-run-compressed-pointer-%s.sh" % param,
                "python build_server_compressed_pointer_%s.py" % param,
                "python dostuff-compressed-pointer-%s.py" % param,
                "/home/user/depot_tools/ninja-linux64 -C /home/user/work/repos/v8/%s" % param,
                "/home/user/depot_tools/ninja-linux64 -C /home/user/work/repos/chrome/%s" % param,
            ]
        else:
            str_list = [
                "bash schedule-run-chrome-%s.sh" % param,
                "python build_server_chrome_%s.py" % param,
                "python dostuff-chrome-%s.py" % param,
                "/home/user/depot_tools/ninja-linux64 -C /home/user/work/repos/chrome/%s" % param,
            ]

        for tmp in str_list:
            command = 'ps aux | grep -E "%s" | grep -v grep' % tmp
            # command = 'ps aux | grep -E "chrome.py|chrome.sh"'
            data = os.popen(command)
            data_list = data.read().splitlines()
            # print(data_list)
            if not data_list:
                continue
            else:
                pid_list = map(lambda x: x.split()[1], data_list)
                print("%s was in operation, its PID is: " % tmp + ",".join(pid_list))
                for pid in pid_list:
                    command = 'kill -9 %s' % str(pid)
                    os.system(command)


if __name__ == '__main__':
    kill_all(argv[1:])
