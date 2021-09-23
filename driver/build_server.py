# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import socket
import json, time
import utils
import builders
from sys import argv
# import resource

LISTEN_ADDRESS = "0.0.0.0"
LISTEN_PORT = int(argv[1]) if argv[1:] else 8799
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((LISTEN_ADDRESS, LISTEN_PORT))
s.listen(5)


def build(config):
    try:
        config = json.loads(config)
    except Exception as e:
        print e
        utils.InitConfig(*(config.split()))
    else:
        utils.InitConfig(**config)
    # Set of engines that get build.
    KnownEngines = []

    if utils.config.has_key('v8'):
        KnownEngines.append(builders.V8())
    if utils.config.has_key('v8-win64'):
        KnownEngines.append(builders.V8Win64())
    if utils.config.has_key('v8-patch'):
        KnownEngines.append(builders.V8_patch())
    if utils.config.has_key('jsc'):
        KnownEngines.append(builders.JavaScriptCore())
    if utils.config.has_key('contentshell'):
        KnownEngines.append(builders.ContentShell())
    if utils.config.has_key('jerryscript'):
        KnownEngines.append(builders.JerryScript())
    if utils.config.has_key('iotjs'):
        KnownEngines.append(builders.IoTjs())
    if utils.config.has_key('chromium-linux'):
        KnownEngines.append(builders.Headless())
    if utils.config.has_key('headless-patch'):
        KnownEngines.append(builders.Headless_patch())
    if utils.config.has_key('chromium-win64'):
        KnownEngines.append(builders.ChromiumWin64())

    # builders.build(KnownEngines, False, False)
    builders.build(KnownEngines, False, True)


while True:
    try:
        sock, addr = s.accept()
        # print "connect", addr
        sock.send("connect ok")
        data = sock.recv(10240)
        if not data:
            print "client close in error with ip " + addr
            continue
        # print "recv", data
        # time.sleep(15)
        build(data)
        sock.send("over")
        sock.close()
        # print "over"
    except Exception, e:
        print e
        try:
            sock.send("error")
        except Exception, e:
            print e
        sock.close()
s.close()
