#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@author:lhj
@time:2019/01/03
"""
import os
import re

import builders
import slaves
import utils
from dostuff_win64 import build

"""
1. 获取到commit id和master号对应的字典；
2. 给定master号的开头和结尾；
3. reset到commit id， 然后build： 如果build成功，××××；如果build失败，×××××××。
4. 得到下一轮的master号，递归运行；
5. 退出条件下一轮mater号与本轮相同或相差1.
"""
base_master_number = 828610
compared_master_number = 828625

base_variance = 0.015
benchmark = "webxprt3"  # in {"speedometer2", "jetstream2", "webxprt3"}
case_name = "__total__"  # "__total__" for total score, or subcase name for subcase score
config_file = "client/tmp/intel-1185g7.config"

base_number = base_master_number
first_variance_number = compared_master_number

DATA_LIST = list()
DATA_DICT = dict()


def reset_src(param):
    if target_os == "win64":
        cmd = 'ssh ' + build_host + ' "powershell /c cd ' + os.path.join(build_repos, Engine.source).replace('\\', '/')\
              + ' ; git reset --hard '+param+'"'
    else:
        cmd = 'cd '+os.path.join(utils.RepoPath, Engine.source)+' ; git reset --hard '+param
    print cmd
    return os.system(cmd)


def remote_test(case_name, shell, env=os.environ.copy(), args=None):
    """
    remote test benchmark, return test result in dict
    """
    cmd = 'ssh '+slave_hostname+' "'
    if target_os == 'win64':
        cmd += 'powershell /c '
    cmd += 'cd '+slave_driver+' ; python remote_test.py %s %s %s"' % (benchmark, shell, target_os)
    print cmd
    ret = os.popen(cmd).read().splitlines()
    print 'ret: ', ret
    ret = map(lambda x: x.split(), ret)
    data = list()
    for x in ret:
        score = x[0]
        name = x[2]
        print(score + '   - ' + name)
        data.append({'name': name, 'time': score})
        if case_name == name:
            result = float(score)

    return result


def binary_search(begin, end, prev=None):
    current = (begin+end)//2
    # exit.
    if begin <= end + 1:
        print (current, prev)
        return
    if reset_src(DATA_DICT[current]):
        raise Exception('reset chromium src error!', current, DATA_DICT[current])

    print "Now build master:%d, commit id:%s" % (current, DATA_DICT[current])
    if build(config_file):
        raise Exception("build error, break!")

    # sync source to remote test slave
    for slave in KnownSlaves:
        slave.prepare([Engine])

    score = remote_test(case_name, shell)
    print case_name, score
    global base_number, first_variance_number
    if standard > 0:
        if score > average:
            # up, current test score larger than average, so the variance happened between base and current
            begin = current
            first_variance_number = current
        else:
            # up, current test score smaller than average, so the variance happened between current and compared
            end = current
            base_number = current
    else:
        if score > average:
            # down, current test score larger than average, so the variance happened between current and compared
            end = current
            base_number = current
        else:
            # down, current test score smaller than average, so the variance happened between base and current
            begin = current
            first_variance_number = current

    binary_search(begin, end, current)


def get_commit_dict():
    if not os.path.exists("%s/log.txt" % utils.DriverPath):
        # special re-direct repo_path
        repo_path = "/repos/chrome/x64/chromium/src"
        os.chdir(repo_path)
        cmd1 = "git log > %s/log.txt" % utils.DriverPath
        if os.system(cmd1):
            print "get chrome git log error!"

    os.chdir(utils.DriverPath)
    with open('log.txt') as f:
        data = f.read()

    reg_string = r'Cr-Commit-Position: refs/heads/master@{#%d}\r?\n[\w\W]*Cr-Commit-Position: refs/heads/master@{#%d}' \
                 % (compared_master_number+1, base_master_number)
    data = re.search(reg_string, data)
    if data:
        with open('c-m.txt', 'w') as f:
            f.write(data.group())

    with open('c-m.txt') as f:
        data = f.read()

    if not data:
        print 'not data!'
        return

    ret = re.findall(r'\ncommit (\w+)[\w\W]*?\n *Cr-Commit-Position: refs/heads/master@{#(\d+)}', data)
    if ret:
        global DATA_LIST, DATA_DICT
        for t in ret:
            DATA_DICT[int(t[1])] = t[0]
            DATA_LIST.append((int(t[1]), t[0]))
    print DATA_LIST
    print len(DATA_LIST), compared_master_number - base_master_number + 1


def prepare():
    print "prepare build environment."
    if target_os == "win64":
        cmd = 'ssh ' + build_host + ' "powershell /c netstat -ano | findstr :'+port+'"'
    else:
        cmd = 'ps aux | grep -E "python build_server.py" | grep -v grep'
    print cmd
    if not os.popen(cmd).read():
        if target_os == 'win64':
            cmd2 = 'python remote_build_server.py %s %s %s > /logs/mixture/build_server_log.txt 2>&1 &' % \
                   (build_driver.replace('\\', '/'), build_host, port)
        else:
            cmd2 = "python build_server.py > /logs/mixture/build_server_log.txt 2>&1 &"
        print cmd2
        if os.system(cmd2):
            print "Start build chrome arm server failed!"


def main():
    try:
        binary_search(compared_master_number, base_master_number)
        print "The error was happended between master number %d and %d:" % (base_number, first_variance_number)
    except Exception as e:
        print e


if __name__ == '__main__':
    utils.InitConfig(config_file)
    target_os = utils.config_get_default('main', 'target_os', 'linux')
    slave = utils.config_get_default('main', 'slaves')
    slave_hostname = utils.config_get_default(slave, 'hostname')
    slave_driver = utils.config_get_default(slave, 'driver')
    slave_repos = utils.config_get_default(slave, 'repos')
    slave_benchmarks = utils.config_get_default(slave, 'benchmarks')

    if target_os == 'win64':
        host = utils.config_get_default('main', 'host')
        port = utils.config_get_default('main', 'port')
        build_host = utils.config_get_default('main', 'build_host')
        build_driver = utils.config_get_default('main', 'build_driver')
        build_repos = utils.config_get_default('main', 'build_repos')

    Engine = None
    if utils.config.has_section('v8'):
        Engine = builders.V8()
    elif utils.config.has_section('v8-win64'):
        Engine = builders.V8Win64()
    elif utils.config.has_section('v8-patch'):
        Engine = builders.V8_patch()
    elif utils.config.has_section('contentshell'):
        Engine = builders.ContentShell()
    elif utils.config.has_section('jerryscript'):
        Engine = builders.JerryScript()
    elif utils.config.has_section('iotjs'):
        Engine = builders.IoTjs()
    elif utils.config.has_section('headless'):
        Engine = builders.Headless()
    elif utils.config.has_section('headless-patch'):
        Engine = builders.Headless_patch()
    elif utils.config.has_section('chromium-win64'):
        Engine = builders.ChromiumWin64()

    shell = os.path.join(utils.RepoPath, Engine.source, Engine.shell())
    rshell = os.path.join(utils.config_get_default(utils.config_get_default('main', 'slaves', None), 'repos', utils.RepoPath), Engine.source, Engine.slave_shell()).replace('\\', '/')
    repo_path = os.path.join(utils.RepoPath, Engine.source)

    # Set of slaves that run the builds.
    KnownSlaves = slaves.init()

    # prepare build environment
    prepare()
    get_commit_dict()

    # double check
    reset_src(DATA_DICT[base_master_number])
    build(config_file)
    for slave in KnownSlaves:
        slave.prepare([Engine])
    base_score = remote_test(case_name, rshell)

    reset_src(DATA_DICT[compared_master_number])
    build(config_file)
    for slave in KnownSlaves:
        slave.prepare([Engine])
    compared_score = remote_test(case_name, rshell)

    average = (base_score + compared_score) / 2
    variance = compared_score / base_score - 1

    if -base_variance < variance < base_variance:
        print "not very large variance, stop."
    else:
        if base_score > compared_score:
            standard = -1
        else:
            standard = 1
        main()
