#!/usr/bin/python
# -*-coding:utf-8-*-
import signal
from sys import argv
import os, sys
import datetime


ERROR_MSG = "ERROR: You can choose one or two or all of the params from 'v8', 'x64' , 'glm'and 'arm', or none param means run them all."


def run_command(param, log_string):
    """
    commands of running different scripts.
    :param param:
    :return:
    """
    logdir = {
        'v8': 'v8',
        'x64': 'chrome/electro',
        'arm': 'chrome/arm',
        'glm': 'chrome/glm'
    }
    if param.lower() not in ['v8', 'x64', 'arm', 'glm']:
        return 1

    log_path = "/home/user/work/logs/%s"%logdir[param.lower()]
    if not os.path.exists(log_path):
        cmd = 'mkdir -p %s'%log_path
        print(cmd)
        if os.system(cmd):
          return 'ERROR: mkdir error.'

    if param.lower() == 'v8':
        str1 = 'python build_server_v8.py > %s/build_server_v8_log%s.txt 2>&1 &' % (log_path, log_string)
        str2 = 'rm -f /tmp/awfy-daemon-v8 /tmp/awfy-lock'
        str3 = 'bash schedule-run-v8.sh > %s/schedule-run-v8-log%s.txt 2>&1 &' % (log_path, log_string)

    elif param.lower() == 'x64':
        str1 = 'python build_server_chrome.py > %s/build_server_chrome_log%s.txt 2>&1 &' % (log_path, log_string)
        str2 = 'rm -f /tmp/awfy-daemon-chrome /tmp/awfy-lock'
        str3 = 'bash schedule-run-chrome.sh > %s/schedule-run-chrome-log%s.txt 2>&1 &' % (log_path, log_string)

    elif param.lower() == 'arm':
        str1 = 'python build_server_chrome_arm.py > %s/build_server_chrome_arm_log%s.txt 2>&1 &' % (log_path, log_string)
        str2 = 'rm -f /tmp/awfy-daemon-chrome-arm /tmp/awfy-lock'
        str3 = 'bash schedule-run-chrome-arm.sh > %s/schedule-run-chrome-arm-log%s.txt 2>&1 &' % (log_path, log_string)

    elif param.lower() == 'glm':
        str1 = 'python build_server_chrome_glm.py > %s/build_server_chrome_glm_log%s.txt 2>&1 &' % (log_path, log_string)
        str2 = 'rm -f /tmp/awfy-daemon-chrome-glm /tmp/awfy-lock'
        str3 = 'bash schedule-run-chrome-glm.sh > %s/schedule-run-chrome-glm-log%s.txt 2>&1 &' % (log_path, log_string)

    else:
        return 1

    print(str1)
    if not os.system(str1):
        print(str2)
        os.system(str2)
        print(str3)
        if not os.system(str3):
            return 0

    return 2


def reset_git(vendor):
    """
    To reset git commit version.
    :param param:
    :return:
    """
    vendor = vendor.lower()

    if vendor not in ['v8', 'x64', 'arm', 'glm']:
        return 1

    try:
        git_rev = get_cur_git_rev(vendor)
    except Exception,e:
        print(e)
        return 2

    if git_rev == 1:
        return 2

    repo = {
        "v8": "/home/user/work/repos/v8",
        "jerryscript": "/home/user/work/repos/jerryscript",
        "x64": "/home/user/work/chromium_repos/chromium/src",
        "glm": "/home/user/work/chromium_glm_repos/chromium/src",
        "arm": "/home/user/work/chromium-arm/chromium/src",
        "home": "/home/user/work/awfy/driver"
    }
    try:
        os.chdir(repo[vendor])
    except Exception as e:
        print(e)
        return 3
    cmd = "git pull && git reset --hard %s" % git_rev
    print cmd
    a = os.system(cmd)
    try:
        os.chdir(repo["home"])
    except:
        return 3
    if a:
        return 3


def interrupted(signum, frame):
    "called when read times out"
    print 'interrupted!'
    signal.signal(signal.SIGALRM, interrupted)


def signal_handler(signum, frame):
    raise Exception("\nTimeout!")


def get_cur_git_rev(vendor):
    """
    get current git commit version.
    :param vendor:
    :return:
    """
    TIMEOUT = 30
    try:
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(TIMEOUT)
        print 'You have 30 seconds to type in your stuff...'
        git_rev = raw_input(
            "Please input the '%s' git_rev, or just press the 'ENTER' key to use the latest git_rev in database: " % vendor)
        signal.alarm(0)
        print "You typed: %s" % git_rev
    except Exception, e:
        print(e)
        git_rev = ''

    if git_rev:
        return git_rev

    query = """SELECT STRAIGHT_JOIN b.cset  
             FROM awfy_run r                                                        
             JOIN awfy_build b ON r.id = b.run_id                                   
             JOIN awfy_score s ON s.build_id = b.id                                 
             JOIN awfy_suite_version v ON v.id = s.suite_version_id                 
             WHERE r.status > 0                                                       
             AND r.machine = %s                                                                                      
             ORDER BY r.stamp DESC;                                                  
             """
    machine = {
        'glm': 11,
        'x64': 10,
        'arm': 9,
        'v8': 8
    }
    sys.path.append("/home/user/work/awfy/server")
    import awfy
    c = awfy.db.cursor()
    c.execute(query, [machine[vendor]])
    try:
        git_rev = c.fetchone()[0].decode('utf-8')
        print(git_rev)
    except Exception as e:
        print(e)
        return 1
    return git_rev


def check_all(param):
    """
    check if the repos was in operation.
    :param repos:
    :return:
    """
    if param.lower() == 'v8':
        str_list = ["python build_server_v8.py", "bash schedule-run-v8.sh", "python dostuff-v8.py"]
    elif param.lower() == 'x64':
        str_list = ["bash schedule-run-chrome.sh", "python build_server_chrome.py", "python dostuff-chrome.py",
                    "/home/user/depot_tools/ninja-linux64 -C /home/user/work/chromium_repos/chromium/src/out/x64 chrome -j40"]
    elif param.lower() == 'arm':
        str_list = ["python build_server_chrome_arm.py", "bash schedule-run-chrome-arm.sh",
                    "python dostuff-chrome-arm.py",
                    "/home/user/depot_tools/ninja-linux64 -C /home/user/work/chromium-arm/chromium/src/out/arm chrome -j40"]
    elif param.lower() == 'glm':
        str_list = ["bash schedule-run-chrome-glm.sh", "python build_server_chrome_glm.py",
                    "python dostuff-chrome-glm.py",
                    "/home/user/depot_tools/ninja-linux64 -C /home/user/work/chromium_glm_repos/chromium/src/out/x64 chrome -j40"]
    else:
        print(ERROR_MSG, "line %d" % sys._getframe().f_lineno)
        return

    run_list = []
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
            run_list.append(tmp)
    else:
        if run_list:
            return run_list
    return 0

def run_related_progress(log_string):
    """
    check the status of apache2 and query_server.py, if they haven't been in operation, start them.
    :return:
    """
    d = {'apache2': "/etc/init.d/apache2 start",
         'query_server.py': "python query_server.py > /home/user/work/logs/query_server_log%s.txt 2>&1 &"%log_string
    }
    for k, v in d.iteritems():
        command = 'ps aux | grep %s | grep -v grep' % k
        data = os.popen(command).read()
        if not data:
            print('Running: %s'%v)
            os.system(v)


def run_list(param, log_string):
    """

    :param param:
    :param logdir:
    :return:
    """
    print("now check if the command you input was already in operation...")
    a = check_all(param.lower())
    if a:
        print("%s is running now!" % str(a))
        return 1
    # r = input("Please check the git commit version of v8 repo source by yourself. \n"
    #           "If you have reset the v8 version to the right version, input 'Y' to continue.")
    # if r.upper() != 'Y':
    #     continue
    print("now reset the git commit version...")
    b = reset_git(param.lower())
    if b == 2:
        print('ERROR: Could not get git commit version!')
        return 1
    elif b == 3:
        print("ERROR: reset git wrong!")
        return 1
    print("run command...")
    t = run_command(param.lower(), log_string)
    return 0


def run_all(repos):
    """
    You can choose params from 'v8', 'x64', 'arm', or none param means run them all.
    functions:
    1. check all progresses to find out if there were some progresses in operation.
    2. reset git commit version.
    3. run command of designated repos.
    :param repo:
    :return:
    """
    log_string = "--" + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    print(log_string)
    # os.system('mkdir /home/user/work/logs/%s'%logdir)

    run_related_progress(log_string)

    if not repos:
        repos = ['v8', 'x64', 'arm', 'glm']
    print(repos)

    for param in repos:
        if param.lower() in ['v8', 'x64', 'arm', 'glm']:
            t = run_list(param.lower(), log_string)
        else:
            t = 1
            print(ERROR_MSG, "line %d" % sys._getframe().f_lineno)

        if t:
            print('check or run command was wrong!')
            continue


if __name__ == '__main__':
    run_all(argv[1:])
    # get_cur_git_rev('x64')
