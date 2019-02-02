#!/usr/bin/python
from sys import argv
import os
import sys


def kill_all(repos):
    """
    kill all progresses of awfy running scripts.
    :param repos:
    :return:
    """
    if not repos:
        return ERROR_MSG
    elif repos == ['all']:
        repos = ['apache2', 'v8', 'arm', 'x64', 'glm', 'query']

    for param in repos:
        if param.lower() == 'apache2':
            cmd = '/etc/init.d/apache2 stop'
            if os.system(cmd):
                print('ERROR: stop apache2 error.')
            continue

        if param.lower() == 'v8':
            str_list = ["python build_server_v8.py", "bash schedule-run-v8.sh", "python dostuff-v8.py"]
        elif param.lower() == 'x64':
            str_list = ["bash schedule-run-chrome.sh", "python build_server_chrome.py", "python dostuff-chrome.py",
                        "/home/user/depot_tools/ninja-linux64 -C /home/user/work/repos/chrome/x64/chromium/src/out/x64 chrome -j40",
                        "ssh user@awfy-x64-spd.sh.intel.com"]
        elif param.lower() == 'arm':
            str_list = ["python build_server_chrome_arm.py", "bash schedule-run-chrome-arm.sh",
                        "python dostuff-chrome-arm.py",
                        "/home/user/depot_tools/ninja-linux64 -C /home/user/work/repos/chrome/arm/chromium/src/out/arm chrome -j40",
                        "ssh user@awfy-arm-spd.sh.intel.com"]
        elif param.lower() == 'glm':
            str_list = ["python build_server_chrome_glm.py", "bash schedule-run-chrome-glm.sh",
                        "python dostuff-chrome-glm.py",
                        "/home/user/depot_tools/ninja-linux64 -C /home/user/work/repos/chrome/glm/chromium/src/out/x64 chrome -j40",
                        "ssh chrx@chrx"]
        elif param.lower() == 'query':
            str_list = ["python query_server.py"]
        else:
            print(ERROR_MSG, "line %d" % sys._getframe().f_lineno)
            return

        for tmp in str_list:
            command = 'ps aux | grep -E "%s" | grep -v grep'%tmp
            # command = 'ps aux | grep -E "chrome.py|chrome.sh"'
            data = os.popen(command)
            data_list = data.read().splitlines()
            # print(data_list)
            if not data_list:
                continue
            else:
                pid_list = map(lambda x: x.split()[1], data_list)
                print("%s was in operation, its PID is: "%tmp + ",".join(pid_list))
                for pid in pid_list:
                    command = 'kill -9 %s'%str(pid)
                    os.system(command)


ERROR_MSG = "ERROR: You can choose one or two or all of the params from 'v8', 'x64', 'arm' and 'apache2'."
if __name__ == '__main__':
    kill_all(argv[1:])
