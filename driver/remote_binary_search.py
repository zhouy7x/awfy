#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@author:lhj
@time:2019/01/03
"""
import os
import re
import socket
import time

import benchmarks
import builders
import utils
from dostuff_win64 import build

"""
1. 获取到commit id和master号对应的字典；
2. 给定master号的开头和结尾；
3. reset到commit id， 然后build： 如果build成功，××××；如果build失败，×××××××。
4. 得到下一轮的master号，递归运行；
5. 退出条件下一轮mater号与本轮相同或相差1.
"""
base_commit_id = "4305bde675647ced2fb1a5782baff01ca089c45b"
base_master_number = 666076
compressed_commit_id = "8ff73bc1bf403515c233a8a09829c0093af32ec2"
compressed_master_number = 666190

benchmark = "speedometer2"  # in {"speedometer2", "jetstream2", "webxprt3"}
case_name = "__total__"  # "__total__" for total score, or subcase name for subcase score
config_file = "client/tmp/intel-1185g7.config"
# src_path = '/repos/chrome/1800x/chromium/src'

base_number = base_master_number
first_variance_number = compressed_master_number

# work_place = '/home/user/work/awfy/driver'

DATA_LIST = list()
DATA_DICT = dict()

# Deprd
# def build(commit_id):
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect(('127.0.0.1', 8799))
#     hello = s.recv(1024)
#     s.sendall(config_file)
#     print '>>>>>>>>>>>>>>>>>>>>>>>>> SENT', config_file
#     reply = s.recv(1024)
#     s.close()
#
#     print '<<<<<<<<<<<<<<<<<<<<<<<< Received', repr(reply)
#
#     # print repr(reply), type(repr(reply)), len(repr(reply))
#
#     if "over" in repr(reply):
#         return 0
#     elif "error" in repr(reply):
#         return 1
#     else:
#         print "WARNING: returned -1!"
#         return -1


def reset_src(param):
    if target_os == "win64":
        cmd = 'ssh ' + build_host + ' "powershell /c cd '+build_repos+' ; git reset --hard '+param
    else:
        cmd = 'cd '+utils.RepoPath+' ; git reset --hard '+param
    print cmd
    return os.system(cmd)


def remote_test(case_name, shell, env=os.environ.copy(), args=None):
    """
    remote test benchmark, return test result in dict
    """
    sp2 = benchmarks.Speedometer2()
    data = sp2.benchmark(shell=shell, env=env, args=args)
    score = float(data[case_name])
    return score


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

    score = remote_test(case_name, shell)
    print case_name, score

    if standard > 0:
        if score > average:
            # up, current test score larger than average, so the variance happened between base and current
            begin = current
            global first_variance_number
            first_variance_number = current
        else:
            # up, current test score smaller than average, so the variance happened between current and compressed
            end = current
            global base_number
            base_number = current
    else:
        if score > average:
            # down, current test score larger than average, so the variance happened between current and compressed
            end = current
            global base_number
            base_number = current
        else:
            # down, current test score smaller than average, so the variance happened between base and current
            begin = current
            global first_variance_number
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

    data = re.search(r'\ncommit %s[\w\W]*Cr-Commit-Position: refs/heads/master@{#%d}' % (compressed_commit_id, base_master_number), data)
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
    print len(DATA_LIST), compressed_master_number - base_master_number + 1


def check_build_process(foo):
    def _inside(*args, **kwargs):
        if target_os == "win64":
            cmd = 'ssh ' + build_host + ' "powershell /c netstat -ano | findstr :8781"'
        else:
            cmd = 'ps aux | grep -E "python build_server.py" | grep -v grep'
        print cmd
        if not os.popen(cmd).read():
            if target_os == 'win64':
                cmd2 = 'python remote_build_server.py %s %s %s > /logs/mixture/build_server_log.txt 2>&1 &' % \
                       (build_driver.replace('\\', '/'), build_host, port)
            else:
                cmd2 = "python build_server.py > /logs/mixture/build_server_log.txt 2>&1 &"
            if os.system(cmd2):
                print "Start build chrome arm server failed!"

        return foo(*args, **kwargs)

    return _inside


@check_build_process
def main():
    get_commit_dict()
    time.sleep(10)

    try:
        binary_search(compressed_master_number, base_master_number)
        print "The error was happended between master number %d and %d:" % (base_number, first_variance_number)
    except Exception as e:
        print e


if __name__ == '__main__':
    utils.InitConfig(config_file)
    target_os = utils.config_get_default('main', 'target_os', 'linux')
    if target_os == 'win64':
        host = utils.config_get_default('main', 'host')
        port = utils.config_get_default('main', 'port')
        build_host = utils.config_get_default('main', 'build_host')
        build_driver = utils.config_get_default('main', 'build_driver')
        build_repos = utils.config_get_default('main', 'build_repos')

    Engine = None
    if utils.config.has_section('v8'):
        Engine = builders.V8()
    if utils.config.has_section('v8-win64'):
        Engine = builders.V8Win64()
    if utils.config.has_section('v8-patch'):
        Engine = builders.V8_patch()
    if utils.config.has_section('contentshell'):
        Engine = builders.ContentShell()
    if utils.config.has_section('jerryscript'):
        Engine = builders.JerryScript()
    if utils.config.has_section('iotjs'):
        Engine = builders.IoTjs()
    if utils.config.has_section('headless'):
        Engine = builders.Headless()
    if utils.config.has_section('headless-patch'):
        Engine = builders.Headless_patch()
    if utils.config.has_section('chromium-win64'):
        Engine = builders.ChromiumWin64()
    shell = os.path.join(utils.RepoPath, Engine.source, Engine.shell())
    repo_path = os.path.join(utils.RepoPath, Engine.source)
    build(base_commit_id)
    base_score = remote_test(case_name, shell)
    build(compressed_commit_id)
    compressed_score = remote_test(case_name, shell)

    average = (base_score + compressed_score) / 2
    variance = compressed_score / base_score - 1

    if -0.03 < variance < 0.03:
        print "not very large variance, stop."
    else:
        if base_score > compressed_score:
            standard = -1
        else:
            standard = 1
        main()
