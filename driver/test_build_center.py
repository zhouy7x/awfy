# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import socket
import json, time
import utils
import builders
import resource
import multiprocessing
import os
from multiprocessing.reduction import reduce_socket, rebuild_socket

LISTEN_ADDRESS = "0.0.0.0"
LISTEN_PORT = 8787
ERROR_LOG_FILE = "/home/user/work/build_server_error.log"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((LISTEN_ADDRESS, LISTEN_PORT))
s.listen(5)

# Set resource limits for child processes
resource.setrlimit(resource.RLIMIT_AS, (-1, -1))
resource.setrlimit(resource.RLIMIT_RSS, (-1, -1))
resource.setrlimit(resource.RLIMIT_DATA, (-1, -1))


def judge_if_build(config):
    utils.InitConfig(config)
    # # Set of engines that get build.
    KnownEngines = []
    if utils.config.has_key('v8'):
        KnownEngines.append(builders.V8())
    if utils.config.has_key('contentshell'):
        KnownEngines.append(builders.ContentShell())
    if utils.config.has_key('jerryscript'):
        KnownEngines.append(builders.JerryScript())
    if utils.config.has_key('iotjs'):
        KnownEngines.append(builders.IoTjs())
    for engine in KnownEngines:
        print "shell: ", os.path.join(utils.RepoPath, engine.source, engine.shell())
        if not os.path.isfile(os.path.join(utils.RepoPath, engine.source, engine.shell())):
            return False
    return True


def build(config):
    time.sleep(3)
    print "build ok with config", config
    utils.InitConfig(config)
    # # Set of engines that get build.
    KnownEngines = []
    if utils.config.has_key('v8'):
        KnownEngines.append(builders.V8())
    if utils.config.has_key('contentshell'):
        KnownEngines.append(builders.ContentShell())
    if utils.config.has_key('jerryscript'):
        KnownEngines.append(builders.JerryScript())
    if utils.config.has_key('iotjs'):
        KnownEngines.append(builders.IoTjs())
    for engine in KnownEngines:
        open(os.path.join(utils.RepoPath, engine.source, engine.shell()), 'a')

    # builders.build(KnownEngines, False, False)


def log_to_file(err_content):
    file = open(ERROR_LOG_FILE, "a+")
    error_log = "error in build_server - %s : %s \n" % (
    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), err_content)
    file.write(error_log)
    file.close()


def build_center(pipe, build_queue, is_building_now):
    while True:
        config = pipe.recv()
        print "build_center recv: ", config
        print "in build_center process:"
        print "in build_center process build_queue ", build_queue

        try:
            build_type = get_build_type(config)
            build(config)
            empty_queue(build_queue[build_type])
            build_queue[build_type] = []
            build_state[build_type] = True
            is_building_now.value = 0
            print "in build_center process build queue after build and clear"
            print "in build_center process build_queue ", build_queue
            # for all jobs in queue, build
            for key in build_queue.keys():
                is_building_now.value = 0
                queue = build_queue[key]
                if len(queue) > 0:
                    is_building_now.value = 1
                    build(queue[0]["config"])
                    empty_queue(queue)
                    build_queue[key] = []
            is_building_now = 0
        except Exception, e:
            is_building_now.value = 0
            log_to_file(str(e))


def empty_queue(queue):
    for i in range(len(queue) - 1, -1, -1):
        s = queue[i]["sock"]
        sock = s[0](*s[1])
        print "socket end", sock
        sock.send("over")
        sock.close()
        del queue[i]


def get_build_type(config_name):
    if "x86" in config_name:
        return "x86"
    if "x64" in config_name:
        return "x64"
    if "arm" in config_name:
        return "arm"
    else:
        raise Error("unsupported type")


def main(build_queue, is_building_now):
    while True:
        try:
            sock, addr = s.accept()
            print "connect", addr
            sock.send("connect ok")
            # commitId = sock.recv(1024)
            data = json.loads(sock.recv(10240))
            config = data["config"]

            print "in main process recv:", config
            print "build queue"
            print "build_queue ", build_queue

            if not data:
                log_to_file("client close in error with ip " + addr)
                continue
            build_type = get_build_type(config)
            print build_type
            # has builded!
            if judge_if_build(config):
                print build_type, "has already build"
                sock.send("over")
                sock.close()
                continue
            # some build_type is building, so put into the build_queue
            if is_building_now.value == 1:
                print "is_building", is_building_now.value
                print "push to queue"
                build_type_queue = build_queue[build_type] if build_type in build_queue else []
                build_type_queue.append({"sock": reduce_socket(sock), "config": config})
                build_queue[build_type] = build_type_queue
                continue
            # no one is building and need build
            print "build queue need to build!!"
            print "build_queue ", build_queue
            is_building_now.value = 1
            build_type_queue = build_queue[build_type] if build_type in build_queue else []
            build_type_queue.append({"sock": reduce_socket(sock), "config": config})
            build_queue[build_type] = build_type_queue

            # sock.send("over")
            # sock.close()
            pipe[1].send(config)
        except Exception, e:
            log_to_file(str(e))
            try:
                sock.send("error")
            except Exception, e:
                print e
            sock.close()
    s.close()


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    build_queue = manager.dict()
    is_building_now = multiprocessing.Value('b', 0)
    pipe = multiprocessing.Pipe()
    schedule_center_process = multiprocessing.Process(target=build_center,
                                                      args=(pipe[0], build_queue, is_building_now,))
    schedule_center_process.start()
    main(build_queue, is_building_now)
