# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import resource
import utils
import time
import socket
from optparse import OptionParser
from collections import namedtuple

import benchmarks
import builders
import puller
import slaves
import submitter

parser = OptionParser(usage="usage: %prog [options] [cset]")
parser.add_option("-c", "--config", dest="config_name", type="string", default="awfy.config",
                  help="Config file (default: awfy.config)")
parser.add_option("-2", "--config2", dest="config2_name", type="string", default="", help="Second config file")
parser.add_option("-3", "--config3", dest="config3_name", type="string", default="", help="Third config file")
(options, progargs) = parser.parse_args()

# print (options, progargs)
# Set resource limits for child processes
resource.setrlimit(resource.RLIMIT_AS, (-1, -1))
resource.setrlimit(resource.RLIMIT_RSS, (-1, -1))
resource.setrlimit(resource.RLIMIT_DATA, (-1, -1))

# A mode is a configuration of an engine we just built.
Mode = namedtuple('Mode', ['shell', 'args', 'env', 'name', 'cset', 'target_os'])


def dostuff(config_name):
    print "dostuff"
    print config_name
    utils.InitConfig(config_name)

    # Set of engines that get build.
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
        # ret['chrome-related'] = True
    if utils.config.has_key('headless-patch'):
        Engine = builders.Headless_patch()
        # ret['chrome-related'] = True
    if utils.config.has_key('chromium-win64'):
        Engine = builders.ChromiumWin64()
        # ret['chrome-related'] = True

    myself = utils.config_get_default('main', 'slaves', '')
    print '>>>>>>>>>>>>>>>>>>>>>>>>> CONNECTING @', myself

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8796))
    hello = s.recv(1024)
    s.sendall(config_name)
    print '>>>>>>>>>>>>>>>>>>>>>>>>> SENT', config_name, '@', myself
    reply = s.recv(1024)
    s.close()

    print '<<<<<<<<<<<<<<<<<<<<<<<< Received', repr(reply), '@', myself

    # The native compiler is a special thing, for now.
    native = builders.NativeCompiler()

    if len(progargs) == 0:
        with utils.FolderChanger(os.path.join(utils.RepoPath, Engine.source)):
            cset = Engine.getPuller().Identify()
    else:
        cset = progargs[0]
    print "***************************************"
    print cset
    print "***************************************"

    # Make a list of all modes.
    modes = []
    shell = os.path.join(utils.RepoPath, Engine.source, Engine.shell())
    target_os = utils.config_get_default('main', 'target_os', 'linux')
    env = None
    with utils.chdir(os.path.join(utils.RepoPath, Engine.source)):
        env = Engine.env()

    modeNames = utils.config_get_default('main', 'modes', None)
    if modeNames:
        modeNames = modeNames.split(",")
        for name in modeNames:
            args = Engine.args[:] if Engine.args else []
            for i in range(1, 100):
                arg = utils.config_get_default(name, 'arg' + str(i), None)
                if arg != None:
                    args.append(arg)
                else:
                    break
            mode = Mode(shell, args, env, name, cset, target_os)
            print myself, name, str(args)
            modes.append(mode)

    # Set of slaves that run the builds. 
    KnownSlaves = slaves.init()

    for slave in KnownSlaves:
        slave.prepare([Engine])

        # Inform AWFY of each mode we found.
        submit = submitter.Submitter(slave)
        print "submit start ..."
        submit.Start()

        for mode in modes:
            print "submit add engine..."
            submit.AddEngine(mode.name, mode.cset)

        # submit.AddEngine(native.mode, native.signature)
        slave.benchmark(submit, native, modes)

    # Wait for all of the slaves to finish running before exiting.
    for slave in KnownSlaves:
        slave.synchronize()


dostuff(options.config_name)

if options.config2_name:
    dostuff(options.config2_name)

if options.config3_name:
    dostuff(options.config3_name)
