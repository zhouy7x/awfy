#!/usr/bin/python
# -*-coding:utf-8-*-
import signal
from sys import argv
import os, sys
import datetime
from devices_config import *


def run_command(param, log_string):
    """
    commands of running different scripts.
    :param param:
    :param log_string:
    :return:
    """
    param = param.lower()
    if param not in ALL_DEVICES:
        return 1

    log_path = "%s/%s" % (LOG_PATH, LOG_DIR[param])
    if not os.path.isdir(log_path):
        cmd = 'rm -rf %s && mkdir -p %s' % (log_path, log_path)
        print(cmd)
        if os.system(cmd):
          return 'ERROR: make log dir error.'
    if param == 'v8':
        str1 = 'python build_server_%s.py > %s/build_server_%s_log%s.txt 2>&1 &' % (param, log_path, param, log_string)
        str2 = 'rm -f /tmp/awfy-daemon-%s /tmp/awfy-lock' % param
        str3 = 'bash schedule-run-%s.sh > %s/schedule-run-%s-log%s.txt 2>&1 &' % (param, log_path, param, log_string)
    elif param in ['cyan', 'bigcore']:
        str1 = 'python build_server_compressed_pointer_%s.py > %s/build_server_compressed_pointer_%s_log%s.txt 2>&1 &' % (param, log_path, param, log_string)
        str2 = 'rm -f /tmp/awfy-daemon-compressed-pointer-%s /tmp/awfy-lock' % param
        str3 = 'bash schedule-run-compressed-pointer-%s.sh > %s/schedule-run-compressed-pointer-%s-log%s.txt 2>&1 &' % (param, log_path, param, log_string)
    else:
        str1 = 'python build_server_chrome_%s.py > %s/build_server_chrome_%s_log%s.txt 2>&1 &' % (param, log_path, param, log_string)
        str2 = 'rm -f /tmp/awfy-daemon-chrome-%s /tmp/awfy-lock' % param
        str3 = 'bash schedule-run-chrome-%s.sh > %s/schedule-run-chrome-%s-log%s.txt 2>&1 &' % (param, log_path, param, log_string)

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
    :param vendor:
    :return:
    """
    git_rev = get_cur_git_rev(vendor)
    os.chdir(REPOS[vendor])

    cmd = "git fetch && git reset --hard %s" % git_rev
    print cmd
    a = os.system(cmd)
    if a:
        raise Exception('git fetch & reset error!')
    os.chdir(REPOS["home"])


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
             """
    if vendor in ['cyan-v8', 'cyan-chrome']:
        query += """
                 AND b.mode_id = %s 
                 """ % MODES[vendor]
    query += """
             ORDER BY r.stamp DESC;                                                  
             """

    sys.path.append("%s/awfy/server" % WORK_DIR)
    import awfy
    c = awfy.db.cursor()
    c.execute(query, [MACHINES[vendor]])

    git_rev = c.fetchone()[0].decode('utf-8')
    print(git_rev)
    return git_rev


def check_all(param):
    """
    check if the repos was in operation.
    :param param:
    :return:
    """
    param = param.lower()
    if param == 'v8':
        str_list = [
            "python build_server_%s.py" % param,
            "bash schedule-run-%s.sh" % param,
            "python dostuff-%s.py" % param
        ]
    elif param in ['cyan', 'bigcore']:
        str_list = [
            "python build_server_compressed_pointer_%s.py" % param,
            "bash schedule-run-compressed-pointer-%s.sh" % param,
            "python dostuff-compressed-pointer-%s.py" % param
        ]
    else:
        str_list = [
            "bash schedule-run-chrome-%s.sh" % param,
            "python build_server_chrome_%s.py" % param,
            "python dostuff-chrome-%s.py" % param,
            "/home/user/depot_tools/ninja-linux64 -C /home/user/work/repos/chrome/%s/chromium/src/out/" % param
        ]

    run_ls = []
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
            print("%s was in operation, its PID is: " % tmp + ",".join(pid_list))
            run_ls.append(tmp)
    else:
        if run_ls:
            return run_ls
    return 0


def run_related_progress():
    """
    check the status of apache2 and query_server.py, if they haven't been in operation, start them.
    :return:
    """
    for k, v in RELATED.iteritems():
        command = 'ps aux | grep %s | grep -v grep' % k
        data = os.popen(command).read()
        if not data:
            print('Running: %s' % v)
            os.system(v)


def run_list(param, log_string):
    """
    :param param:
    :param log_string:
    :return:
    """
    print("now check if the command you input was already in operation...")
    param = param.lower()
    run_ls = check_all(param)
    if run_ls:
        print("%s is running now!" % str(run_ls))
        return 1

    print("now reset the git commit version...")
    try:
        if param == 'cyan':
            params = ['cyan-v8', 'cyan-chrome']
            for tmp in params:
                reset_git(tmp)
        else:
            reset_git(param)
    except Exception as e:
        print e
        return 1
    print("run command...")
    run_command(param, log_string)
    return 0


def run_all(repos):
    """
    You can choose params from %s, or none param means run them all.
    functions:
    1. check all progresses to find out if there were some progresses in operation.
    2. reset git commit version.
    3. run command of designated repos.
    :param repos:
    :return:
    """
    log_string = "--" + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    print(log_string)
    # os.system('mkdir /home/user/work/logs/%s'%logdir)
    run_related_progress()

    if not repos:
        repos = ALL_DEVICES
    print(repos)

    for param in repos:
        param = param.lower()
        if param in ALL_DEVICES:
            t = run_list(param, log_string)
        else:
            t = 1
            print(ERROR_MSG)

        if t:
            print('check or run command was wrong!')
            continue


if __name__ == '__main__':
    run_all(argv[1:])
    # get_cur_git_rev('x64')
