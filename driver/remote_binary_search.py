#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@author:zy
@time:2021/04/07
"""
import json
import os
import re
import sys

import builders
import slaves
import utils
from dostuff import build
"""
1. 获取到commit id和master号对应的字典；
2. 给定master号的开头和结尾；
3. reset到commit id， 然后build： 如果build成功，××××；如果build失败，×××××××。
4. 得到下一轮的master号，递归运行；
5. 退出条件下一轮mater号与本轮相同或相差1.
"""
base_master_number = 1069647
compared_master_number = 1070487

# 1.bisect special config
mode = "headless"
benchmark = "jetstream21"  # in {"speedometer2", "jetstream2", "webxprt3"}
case_name = "HashSet-wasm"  # "__total__" for total score, or the name of subcase for subcase score
file_name = "client/tmp/intel-8700k.config"

# 2.save config to debug json file.
# 2.1 device name
device_config = utils.debug_config_to_dict(file_name)
file_path = file_name[:file_name.rfind('/')+1]
mode_name = file_name[file_name.rfind('/')+1:].split('.')[0]
device_config['name'] = mode_name
# 2.2 test mode
device_config['main']['modes'] = mode
# 2.3 test benchmark
slave_name = device_config['main']['slaves']
device_config[slave_name]['includes'] = benchmark
# 2.4 save to device type config
config = dict()
device_type = 'debug'
config[device_type] = [device_config]
# 2.5 save to config file
debug_config_json_path = os.path.join(file_path, mode_name+'.json')
with open(debug_config_json_path, 'w') as f:
    f.write(json.dumps(config))
# 2.6 build init config dict:
# device_type, mode_name=None, mode_startswith=None, is_debug=False, debug_config_path="client/tmp/config.json"
build_config = dict()
build_config['device_type'] = device_type
build_config['mode_name'] = mode_name
build_config['is_debug'] = True
build_config['debug_config_path'] = debug_config_json_path

# 3.bisect base config
log_repo_path = "/home/user/work/repos/chrome/x64/chromium/src"
base_variance = 0.015
base_number = base_master_number
first_variance_number = compared_master_number
DATA_DICT = dict()


def reset_src(param, fetch=False):
    if target_os == "win64":
        cmd = 'ssh ' + build_host + ' "powershell /c cd ' + os.path.join(build_repos, Engine.source).replace('\\', '/')
        cmd = 'ssh ' + build_host + ' "cd ' + os.path.join(build_repos, Engine.source).replace('\\', '/')
        if fetch:
            cmd += ' ; git fetch'
        cmd += ' ; git reset --hard '+param+'"'
    else:
        cmd = 'cd '+os.path.join(utils.RepoPath, Engine.source)+' ; git reset --hard '+param
    print(cmd)
    return os.system(cmd)


def remote_test(case_name, shell, env=os.environ.copy()):
    """
    remote test benchmark, return test result in dict
    """
    cmd = 'ssh '+slave_hostname+' "'
    if target_os == 'win64':
        cmd += 'powershell /c '
    cmd += 'cd '+slave_driver+' ; python remote_test.py %s %s %s ' % (benchmark, shell, target_os)
    # add args
    modeName = utils.config_get_default('main', 'modes', None)
    args = Engine.args[:] if Engine.args else []
    if modeName:
        for i in range(1, 100):
            arg = utils.config_get_default(modeName, 'arg' + str(i), None)
            if arg != None:
                args.append(arg)
            else:
                break
    if args:
        cmd += ' '.join(args)
    cmd += ' "'
    print(cmd)
    ret = os.popen(cmd).read().splitlines()
    print('ret: ', ret)
    ret = map(lambda x: x.split(), ret)
    data = list()
    for x in ret:
        try:
            score = x[0]
            name = x[2]
            print(score + '   - ' + name)
            data.append({'name': name, 'time': score})
            if case_name == name:
                result = float(score)
        except IndexError as e:
            continue
    return result


def binary_search(begin, end, prev=None):
    current = (begin+end)//2
    # exit.
    if begin <= end + 1:
        # print(current, prev)
        return
    if reset_src(DATA_DICT[current]):
        raise Exception('reset chromium src error!', current, DATA_DICT[current])

    print("Now build master:%d, commit id:%s" % (current, DATA_DICT[current]))
    if build(**build_config):
        raise Exception("build error, break!")

    # sync source to remote test slave
    for slave in KnownSlaves:
        slave.prepare([Engine])

    score = remote_test(case_name, rshell)
    print("'" + case_name + "' of benchmark: '" + benchmark + "' in master number: '" + str(current) +
          "' is: " + str(score))
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

    print('\n'+'*'*60)
    print("Now binary search between %d and %d!" % (base_number, first_variance_number))
    binary_search(begin, end, current)


def get_commit_dict(run_clean=False):
    os.system('rm -rf c-m.txt')
    if run_clean:
        os.system('rm -rf log.txt')
    if run_clean or not os.path.exists("%s/log.txt" % utils.DriverPath):
        # special re-direct repo_path
        # repo_path = "/repos/chrome/x64/chromium/src"
        os.chdir(log_repo_path)
        os.system("git reset --hard ; git pull")
        cmd1 = "git log > %s/log.txt" % utils.DriverPath
        if os.system(cmd1):
            print("get chrome git log error!")

    os.chdir(utils.DriverPath)
    with open('log.txt') as f:
        data = f.read()

    reg_string = r'Cr-Commit-Position: refs/heads/(master|main)@{#%d}\r?\n\r?\ncommit[\w\W]*Cr-Commit-Position: refs/heads/(master|main)@{#%d}' \
                 % (compared_master_number+1, base_master_number)
    data = re.search(reg_string, data)
    if data:
        with open('c-m.txt', 'w') as f:
            f.write(data.group())

    if not os.path.exists('c-m.txt'):
        print('no c-m.txt!')
        return
    with open('c-m.txt') as f:
        data = f.read()
    if not data:
        print('no data!')
        return

    ret = re.findall(r'\ncommit (\w+)[\w\W]*?\n *Cr-Commit-Position: refs/heads/(master|main)@{#(\d+)}', data)
    if ret:
        global DATA_DICT
        for t in ret:
            DATA_DICT[int(t[2])] = t[0]
    print(DATA_DICT)
    print("Length of commit ids found | Length of master numbers given")
    print(str(len(DATA_DICT)).center(26, ' '), '|', str(compared_master_number-base_master_number+1).center(29, ' '))


def prepare(remote_rsync, target_os, driver_path):
    print("Prepare build environment.")
    # 1.Rsync to build server if remote build.
    if remote_rsync:
        build_driver = utils.config_get_default('build', 'driver', utils.DriverPath)
        print(build_driver)
        # for windows translate path format
        if target_os in ['win64']:
            reger = re.match(r"^(\w):(.*)$", build_driver)
            if reger:
                tmp = reger.groups()
                build_driver = "/cygdrive/" + tmp[0] + tmp[1]
                build_driver = build_driver.replace('\\', '/')
                print(build_driver)
        rsync_flags = "-aP"
        try:
            ssh_port = int(utils.config_get_default('build', 'ssh_port', 22))
        except:
            raise Exception("could not get ssh port!")
        else:
            if ssh_port != 22:
                rsync_flags += " -e 'ssh -p "+str(ssh_port)+"'"
            sync_cmd = ["rsync", rsync_flags]
            sync_cmd += [driver_path, build_host+':'+os.path.dirname(build_driver)]
            utils.Run(sync_cmd)
    # 2.Check if build server and test client are in the known_hosts.
    # TODO
    # if utils.RemoteBuild:
    #     cmd1 = 'ssh ' + build_host
    #     print(cmd1)
    #     os.system(cmd1)
    # cmd2 = 'ssh ' + slave_hostname
    # print(cmd2)
    # os.system(cmd2)
    # 3.Check build process.
    if utils.RemoteBuild and target_os == "win64":
        cmd = 'ssh ' + build_host + ' "powershell /c netstat -ano | findstr :'+str(port)+'"'
    else:
        cmd = 'ps aux | grep -E "python build_server.py %d" | grep -v grep' % port
    print(cmd)
    if not os.popen(cmd).read():
        if target_os == 'win64':
            # Start remote build server.
            cmd2 = 'python remote_build_server.py --device-type=%s --is-debug=%s --config=%s > ' \
                   '/logs/mixture/build_server_log.txt 2>&1 &' % (device_type, 'true', debug_config_json_path)
        else:
            cmd2 = "python build_server.py %s > /logs/mixture/build_server_log.txt 2>&1 &" % port
        print(cmd2)
        if os.system(cmd2):
            print("Start build chrome arm server failed!")


def main():
    try:
        binary_search(compared_master_number, base_master_number)
        print("*" * 33 + "FINAL" + "*" * 33)
        print("The variance or error was happended between master number %d and %d." % (base_number, first_variance_number))
        print("*" * 33 + "OVER" + "*" * 33)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    utils.InitConfig(**build_config)
    # main config
    target_os = utils.TargetOS
    driver_path = utils.DriverPath
    port = utils.BuildPort
    host = utils.BuildHost
    # slave config
    slave = utils.config_get_default('main', 'slaves')
    slave_hostname = utils.config_get_default(slave, 'hostname')
    slave_driver = utils.config_get_default(slave, 'driver')
    slave_repos = utils.config_get_default(slave, 'repos')
    slave_benchmarks = utils.config_get_default(slave, 'benchmarks')

    # remote build config
    if utils.RemoteBuild:
        build_repos = utils.config_get_default('build', 'repos', utils.RepoPath)
        build_driver = utils.config_get_default('build', 'driver', utils.DriverPath)
        build_host = utils.config_get_default('build', 'hostname', None)

    Engine = None
    if utils.config.has_key('v8'):
        Engine = builders.V8()
    if utils.config.has_key('v8-win64'):
        Engine = builders.V8Win64()
    if utils.config.has_key('v8-patch'):
        Engine = builders.V8_patch()
    if utils.config.has_key('contentshell'):
        Engine = builders.ContentShell()
    if utils.config.has_key('jerryscript'):
        Engine = builders.JerryScript()
    if utils.config.has_key('iotjs'):
        Engine = builders.IoTjs()
    if utils.config.has_key('chromium-linux'):
        Engine = builders.Headless()
    if utils.config.has_key('headless-patch'):
        Engine = builders.Headless_patch()
    if utils.config.has_key('chromium-win64'):
        Engine = builders.ChromiumWin64()

    # shell = os.path.join(utils.RepoPath, Engine.source, Engine.shell())
    if target_os == 'win64':
        rshell = os.path.join(utils.config_get_default(utils.config_get_default('main', 'slaves', None), 'repos', utils.RepoPath), Engine.source, Engine.slave_shell()).replace('\\', '/')
    else:
        rshell = os.path.join(utils.config_get_default(utils.config_get_default('main', 'slaves', None), 'repos', utils.RepoPath), Engine.source, Engine.shell())
    repo_path = os.path.join(utils.RepoPath, Engine.source)

    # Set of slaves that run the builds.
    KnownSlaves = slaves.init()

    # prepare build environment
    param = sys.argv[1] if sys.argv[1:] else None
    run_clean = False
    if param == 'clean':
        run_clean = True
    prepare(remote_rsync=utils.RemoteRsync, target_os=target_os, driver_path=driver_path)
    get_commit_dict(run_clean)

    # double check if the regression or improvement exists.
    reset_src(DATA_DICT[base_master_number], fetch=True)
    build(**build_config)
    for slave in KnownSlaves:
        slave.prepare([Engine])
    base_score = remote_test(case_name, rshell)
    print('base_score:', base_score)
    print("*" * 60)

    reset_src(DATA_DICT[compared_master_number])
    build(**build_config)
    for slave in KnownSlaves:
        slave.prepare([Engine])
    compared_score = remote_test(case_name, rshell)
    print('compared_score:', compared_score)
    print("*" * 60)

    print('base_master_number: %d, compared_master_number: %d' % (base_master_number, compared_master_number))
    print('base_score: %f, compared_score: %f' % (base_score, compared_score))

    average = (base_score + compared_score) / 2
    variance = compared_score / base_score - 1
    print("*"*66)
    print("The variance double checked is: ", variance)
    print("*"*66)
    if -base_variance < variance < base_variance:
        # the variance is too small or unstable, cannot find it out
        print("The variance is smaller than defined limit variance: %d. Shut down process!" % variance)
    else:
        if base_score > compared_score:
            standard = -1
        else:
            standard = 1
        main()
