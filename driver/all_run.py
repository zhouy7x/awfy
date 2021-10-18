#!/usr/bin/python
# -*-coding:utf-8-*-
import signal
import time
from sys import argv
import os, sys
import datetime
import utils

run_fetch = True
RELATED = {
    'apache2': "/etc/init.d/apache2 start",
    'query_server.py': "python query_server.py > %s/query_server_log.txt 2>&1 &" % utils.LOG_PATH
}
TIMEOUT = 30
ERROR_MSG = "ERROR: You can choose one or two or all of the params from %s, " \
            "or none param means run them all." % ','.join(utils.ALL_DEVICES)


def check_build_server_status(tmp):
    index = tmp.find(" >")
    if index > 0:
        process_string = tmp[:index]
    else:
        process_string = ' '.join(tmp.split()[:-3])
    time.sleep(2)
    command = 'ps ax | grep -E "%s" | grep -v grep' % process_string
    data = os.popen(command).read()
    # print(data_list)
    if not data:
        print "ERROR: start %s failed, retry..." % tmp
        return 1
    else:
        print data
        return 0


def run_command(param, log_string):
    """
    commands of running different scripts.
    :param param:
    :param log_string:
    :return:
    """
    param = param.lower()
    if param not in utils.ALL_DEVICES:
        return 1

    log_path = os.path.join(utils.LOG_PATH, param)
    if not os.path.isdir(log_path):
        cmd = 'rm -rf %s && mkdir -p %s' % (log_path, log_path)
        print(cmd)
        if os.system(cmd):
            return 'ERROR: make log dir error.'
    if param in ['jsc', 'win64']:
        # TODO: device config must link to config file, not other, must get config from config file, not default params.
        str1 = 'python remote_build_server.py -d %s > %s/build_server_%s_log%s.txt 2>&1 &' % (param, log_path, param, log_string)
        str2 = 'rm -f /tmp/awfy-daemon-%s /tmp/awfy-lock' % param
        str3 = 'bash schedule-run-%s.sh > %s/schedule-run-%s-log%s.txt 2>&1 &' % (param, log_path, param, log_string)
    elif param in ['v8', '1800x', 'x64', '3800x']:
        str1 = 'python build_server_%s.py > %s/build_server_%s_log%s.txt 2>&1 &' % (param, log_path, param, log_string)
        str2 = 'rm -f /tmp/awfy-daemon-%s /tmp/awfy-lock' % param
        str3 = 'bash schedule-run-%s.sh > %s/schedule-run-%s-log%s.txt 2>&1 &' % (param, log_path, param, log_string)
    elif param in ['cyan', 'bigcore']:
        str1 = 'python build_server_compressed_pointer_%s.py > %s/build_server_compressed_pointer_%s_log%s.txt 2>&1 &' % (param, log_path, param, log_string)
        str2 = 'rm -f /tmp/awfy-daemon-%s /tmp/awfy-lock' % param
        str3 = 'bash schedule-run-compressed-pointer-%s.sh > %s/schedule-run-compressed-pointer-%s-log%s.txt 2>&1 &' % (param, log_path, param, log_string)
    else:
        str1 = 'python build_server_chrome_%s.py > %s/build_server_chrome_%s_log%s.txt 2>&1 &' % (param, log_path, param, log_string)
        str2 = 'rm -f /tmp/awfy-daemon-chrome-%s /tmp/awfy-lock' % param
        str3 = 'bash schedule-run-chrome-%s.sh > %s/schedule-run-chrome-%s-log%s.txt 2>&1 &' % (param, log_path, param, log_string)

    print(str1)
    if not os.system(str1):
        if not check_build_server_status(str1):
            print(str2)
            os.system(str2)
            print(str3)
            if not os.system(str3):
                return 0
        else:
            return 3
    return 2


def reset_git(vendor, mode_startswith=None):
    """
    To reset git commit version.
    :param vendor:
    :param mode_startswith:
    :return:
    """
    utils.InitConfig(vendor, mode_startswith=mode_startswith)
    git_rev = get_cur_git_rev(vendor, mode_startswith=mode_startswith)
    source = utils.config_get_default(utils.config_get_default('main', 'source'), 'source')
    if utils.RemoteBuild:
        BuildHost = utils.config_get_default('build', 'hostname')
        BuildRepoPath = utils.config_get_default('build', 'repos', utils.RepoPath)
        repo_path = os.path.join(BuildRepoPath, source)
        cmd = 'ssh '
        try:
            ssh_port = int(utils.config_get_default('build', 'ssh_port', 22))
        except:
            raise Exception("could not get ssh port!")

        if ssh_port != 22:
            cmd += '-p ' + str(ssh_port) + ' '

        cmd += BuildHost + ' "cd ' + repo_path + ' ; git fetch ; git reset --hard ' + git_rev + '"'
        print cmd
        a = os.system(cmd)
    else:
        repo_path = os.path.join(utils.RepoPath, source)
        with utils.chdir(repo_path):
            print(">> Executing in " + os.getcwd())
            if run_fetch:
                os.system("git fetch")
            cmd = "git reset --hard %s" % git_rev
            print cmd
            a = os.system(cmd)
    if a:
        raise Exception('git fetch or reset error!')


def interrupted(signum, frame):
    """called when read times out"""
    print 'interrupted!'
    signal.signal(signal.SIGALRM, interrupted)


def signal_handler(signum, frame):
    raise Exception("\nTimeout!")


def get_cur_git_rev(vendor, mode_startswith=None):
    """
    get current git commit version.
    :param vendor:
    :return:
    """
    try:
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(TIMEOUT)
        print 'You have 30 seconds to type in your stuff...'
        msg = "Please input the '%s' " % vendor
        if mode_startswith:
            msg += "'" + mode_startswith + "'"
        msg += " git_rev, or just press the 'ENTER' key to use the latest git_rev in database: "
        git_rev = raw_input(msg)
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
             JOIN awfy_mode m ON m.id = b.mode_id 
             WHERE r.status > 0 
             AND r.machine = %s 
             """
    if mode_startswith:
        query += """
                 AND m.mode = "%s" 
                 """ % utils.MODES[0]
    query += """
             ORDER BY r.stamp DESC;                                                  
             """

    sys.path.append("%s/awfy/server" % utils.WORK_DIR)
    import awfy
    c = awfy.db.cursor()
    machine_id = utils.config_get_default(utils.config_get_default('main', 'slaves'), 'machine')
    c.execute(query, [machine_id])

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
    if param in ['jsc', 'win64']:
        str_list = [
            "python remote_build_server.py -d %s" % param,
            "bash schedule-run-%s.sh" % param,
            "python dostuff_%s.py" % param
        ]
    elif param in ['v8', '1800x', 'x64', '3800x']:
        str_list = [
            "python build_server_%s.py" % param,
            "bash schedule-run-%s.sh" % param,
            "python dostuff_%s.py" % param
        ]
    elif param in ['cyan', 'bigcore']:
        str_list = [
            "python build_server_compressed_pointer_%s.py" % param,
            "bash schedule-run-compressed-pointer-%s.sh" % param,
            "python dostuff_compressed_pointer_%s.py" % param
        ]
    else:
        str_list = [
            "bash schedule-run-chrome-%s.sh" % param,
            "python build_server_chrome_%s.py" % param,
            "python dostuff_chrome_%s.py" % param,
            "/home/user/depot_tools/ninja-linux64 -C /home/user/work/repos/chrome/%s/chromium/src/out/" % param
        ]
    # kill remote build process.
    if param in ['jsc', 'win64']:
        from remote_build_server import kill_processes
        kill_processes(param)
    # check process pids.
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
    netstat -ano | findstr :8781
    taskkill /f /pid 4400
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
        if param in ['cyan', '1800x', '3800x', 'bigcore', 'x64', 'win64']:
            # params = ['%s-v8' % param, '%s-chrome' % param]
            mode_startswith = ['v8', 'chrome']
            for tmp in mode_startswith:
                reset_git(param, tmp)
        else:
            reset_git(param)
    except Exception as e:
        print e
        return 1
    print("run command...")
    if run_command(param, log_string) == 3:
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

    # Deprecated
    # if 'review' in repos:
    #     # for 'review', must reset system time outside docker container,
    #     # `sudo date --set="2021-01-01 22:22:22" ; sudo hwclock --systohc`
    #     prepare_cmd = "patch -p1 -i patch/run-review.patch"
    #     repos = REVIEW_DEVICES
    #     global run_fetch
    #     run_fetch = False
    # else:
    #     prepare_cmd = "patch -p1 -i patch/run-latest.patch"
    # utils.RunTimedCheckOutput(prepare_cmd, timeout=5)
    # # clean patch failed log
    # os.system("rm -rf ./*.rej ./*.orig")

    if not repos:
        repos = utils.ALL_AVAILABLE_DEVICES
    print(repos)
    if 'prepare' in repos:
        return

    for param in repos:
        param = param.lower()
        if param not in utils.ALL_DEVICES:
            t = 1
            print(ERROR_MSG)
        else:
            t = run_list(param, log_string)

        if t:
            print('check or run command was wrong!')
            continue


if __name__ == '__main__':
    run_all(argv[1:])
    # get_cur_git_rev('x64')
