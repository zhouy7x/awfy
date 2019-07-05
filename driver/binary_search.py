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

"""
1. 获取到commit id和master号对应的字典；
2. 给定master号的开头和结尾；
3. reset到commit id， 然后build： 如果build成功，××××；如果build失败，×××××××。
4. 得到下一轮的master号，递归运行；
5. 退出条件下一轮mater号与本轮相同或相差1.
"""
end_id = "4305bde675647ced2fb1a5782baff01ca089c45b"
end_master = 666076
begin_id = "8ff73bc1bf403515c233a8a09829c0093af32ec2"
begin_master = 666190
err_id = begin_master
ok_id = end_master

config_name = "client/machine_config/elm-arm.config"
work_place = '/home/user/work/awfy/driver'
src_path = '/repos/chrome/arm/chromium/src'

DATA_LIST = list()
DATA_DICT = dict()


def build(commit_id):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8795))
    hello = s.recv(1024)
    s.sendall(config_name)
    print '>>>>>>>>>>>>>>>>>>>>>>>>> SENT', config_name
    reply = s.recv(1024)
    s.close()

    print '<<<<<<<<<<<<<<<<<<<<<<<< Received', repr(reply)

    # print repr(reply), type(repr(reply)), len(repr(reply))

    if "over" in repr(reply):
        return 0
    elif "error" in repr(reply):
        return 1
    else:
        print "WARNING: returned -1!"
        return -1


def reset_src(param):
    os.chdir(src_path)
    cmd = 'git reset --hard %s' % param
    return os.system(cmd)


def binary_search(begin, end, prev=None):
    now = (begin+end)//2
    # exit.
    if begin <= end + 1:
        # print (now, prev)
        return
    if reset_src(DATA_DICT[now]):
        raise Exception('reset chromium src error!', now, DATA_DICT[now])

    print "Now build master:%d, commit id:%s" % (now, DATA_DICT[now])
    if build(DATA_DICT[now]):
        # 有值，说明编译失败，往后找
        begin = now
        global err_id
        err_id = now
    else:
        # 编译成功， 往前找
        end = now
        global ok_id
        ok_id = now

    binary_search(begin, end, now)


def get_commit_dict():
    if not os.path.exists("%s/log.txt" % work_place):
        os.chdir(src_path)
        cmd1 = "git log > %s/log.txt" % work_place
        if os.system(cmd1):
            print "get chrome git log error!"

    os.chdir(work_place)
    with open('log.txt') as f:
        data = f.read()

    data = re.search(r'\ncommit %s[\w\W]*Cr-Commit-Position: refs/heads/master@{#%d}' % (begin_id, end_master), data)
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
    # print DATA_LIST
    # print len(DATA_LIST), begin_master - end_master + 1


def check_build_process(foo):
    def _inside(*args, **kwargs):
        cmd = 'ps aux | grep -E "python build_server_chrome_arm.py" | grep -v grep'
        if not os.popen(cmd).read():
            cmd2 = "python build_server_chrome_arm.py > /logs/chrome/arm/build_server_chrome_arm_log.txt 2>&1 &"
            if os.system(cmd2):
                print "Start build chrome arm server failed!"

        return foo(*args, **kwargs)

    return _inside


@check_build_process
def main():
    get_commit_dict()
    time.sleep(10)
    try:
        binary_search(begin_master, end_master)
        print "The error was happended between master number %d and %d:" % (ok_id, err_id)
    except Exception as e:
        print e


if __name__ == '__main__':
    main()
