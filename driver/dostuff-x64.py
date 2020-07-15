# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import resource
import utils
import time
import socket
import threading
from optparse import OptionParser
from collections import namedtuple

import builders
import slaves
import submitter

parser = OptionParser(usage="usage: %prog [options] [cset]")
parser.add_option("-c", "--config", dest="config_name", type="string", default="awfy.config",
                  help="Config file (default: awfy.config)")
parser.add_option("-2", "--config2", dest="config2_name", type="string", default="", help="Second config file")
parser.add_option("-3", "--config3", dest="config3_name", type="string", default="", help="Third config file")
(options, progargs) = parser.parse_args()
print (options, progargs)

# Set resource limits for child processes
resource.setrlimit(resource.RLIMIT_AS, (-1, -1))
resource.setrlimit(resource.RLIMIT_RSS, (-1, -1))
resource.setrlimit(resource.RLIMIT_DATA, (-1, -1))

# A mode is a configuration of an engine we just built.
Mode = namedtuple('Mode', ['shell', 'args', 'env', 'name', 'cset'])


def build(config_name):
    print('build')
    utils.InitConfig(config_name)
    myself = utils.config_get_default('main', 'slaves', '')
    print '>>>>>>>>>>>>>>>>>>>>>>>>> CONNECTING @', myself

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8794))
    hello = s.recv(1024)
    s.sendall(config_name)
    print '>>>>>>>>>>>>>>>>>>>>>>>>> SENT', config_name, '@', myself
    reply = s.recv(1024)
    # time.sleep(5)
    # reply = 'reply'
    s.close()
    print '<<<<<<<<<<<<<<<<<<<<<<<< Received', repr(reply), '@', myself


def dostuff(config_name, Engine):
    print "dostuff"
    print config_name
    utils.InitConfig(config_name)
    myself = utils.config_get_default('main', 'slaves', '')

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
            mode = Mode(shell, args, env, name, cset)
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


def get_config_to_dict(config):
    utils.InitConfig(config)
    # Set of engines that get build.
    Engine = None

    if utils.config.has_section('v8'):
        Engine = builders.V8()
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

    ret = dict()
    ret['cpu'] = utils.config.get('main', 'cpu')
    ret['RepoPath'] = utils.RepoPath
    ret['modes'] = utils.config.get('main', 'modes')
    ret['hostname'] = utils.config.get(utils.config.get('main', 'slaves'), 'hostname')
    ret['source'] = Engine.source
    ret['engine'] = Engine
    return ret


config1 = get_config_to_dict(options.config_name)
build(options.config_name)
thread1 = threading.Thread(target=dostuff, args=(options.config_name, config1['engine']))
thread1.start()
# dostuff(options.config_name)

if options.config2_name:
    config2 = get_config_to_dict(options.config2_name)
    # if build the same chrome, skip build step.
    if config2['cpu'] != config1['cpu'] or config2['RepoPath'] != config1['RepoPath'] or \
            config2['modes'] != config1['modes'] or config2['source'] != config1['source']:
        build(options.config2_name)
    if config2['hostname'] == config1['hostname']:
        print "before thread2, thread1 join"
        thread1.join()

    thread2 = threading.Thread(target=dostuff, args=(options.config2_name, config2['engine']))
    thread2.start()

if options.config3_name:
    config3 = get_config_to_dict(options.config3_name)
    # if build the same chrome, skip build step.
    if config3['cpu'] != config1['cpu'] or config3['RepoPath'] != config1['RepoPath'] or \
            config3['modes'] != config1['modes'] or config3['source'] != config1['source']:
        if options.config2_name:
            if config3['cpu'] != config2['cpu'] or config3['RepoPath'] != config2['RepoPath'] or \
                    config3['modes'] != config2['modes'] or config3['source'] != config2['source']:
                    build(options.config3_name)
        else:
            build(options.config3_name)

    # if remote run in the same slave, wait until previous thread over.
    if config3['hostname'] == config1['hostname']:
        print "before thread3, thread1 join"
        thread1.join()
    if options.config2_name:
        if config3['hostname'] == config2['hostname']:
            print "before thread3, thread2 join"
            thread2.join()

    thread3 = threading.Thread(target=dostuff, args=(options.config3_name, config3['engine']))
    thread3.start()

thread1.join()
if options.config2_name:
    thread2.join()
if options.config3_name:
    thread3.join()
