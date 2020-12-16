# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import re
import resource
import utils
import time
import socket
# import threading
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
Mode = namedtuple('Mode', ['shell', 'args', 'env', 'name', 'cset', 'target_os'])


def rsync_to_local(src, dest):
    # if not os.path.isdir(dest):
    os.system("rm -rf "+dest)
    os.system("mkdir -p "+dest)
    cmd = ["rsync", "-aP"]
    cmd.append(src)
    cmd.append(dest)
    print cmd
    utils.Run(cmd)


def build(config_name):
    print('build')
    print(config_name)
    utils.InitConfig(config_name)
    myself = utils.config_get_default('main', 'slaves', '')
    print '>>>>>>>>>>>>>>>>>>>>>>>>> CONNECTING @', myself

    # sync build driver with local.
    build_driver = utils.config_get_default('main', 'build_driver', None)
    DriverPath = utils.DriverPath
    if build_driver != DriverPath:
        build_host = utils.config_get_default('main', 'build_host')
        print build_driver
        reger = re.match(r"^(\w):(.*)$", build_driver)
        if reger:
            tmp = reger.groups()
            # print tmp
            build_driver = "/cygdrive/" + tmp[0] + tmp[1]
            build_driver = build_driver.replace('\\', '/')
            print build_driver
        rsync_flags = "-aP"
        sync_cmd = ["rsync", rsync_flags]
        sync_cmd += [DriverPath, build_host+':'+os.path.dirname(build_driver)]
        utils.Run(sync_cmd)

    # start build
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = utils.config_get_default('main', 'host', '127.0.0.1')
    try:
        port = int(utils.config_get_default('main', 'port'))
    except:
        raise Exception("could not get port!")

    s.connect((host, port))
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
    print '>>>>>>>>>>>>>>>>>>>>>>>>> CONNECTING @', myself

    # The native compiler is a special thing, for now.
    native = builders.NativeCompiler()

    if len(progargs) == 0:
        # TODO: get cset from remote build server.
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
    with utils.chdir(os.path.join(utils.RepoPath, Engine.source.replace('\\', '/'))):
        env = Engine.env()

    modeNames = utils.config_get_default('main', 'modes', None)
    if modeNames:
        modeNames = modeNames.split(",")
        for name in modeNames:
            if target_os == "win64":
                shell = os.path.join(utils.config_get_default(utils.config_get_default('main', 'slaves'), 'repos'), Engine.source, Engine.slave_shell())
                shell = shell.replace('/', '\\')
                print 'mode.shell: '+shell
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


def get_config_to_dict(config):
    print 'get_config_to_dict'
    print config
    utils.InitConfig(config)
    # Set of engines that get build.
    ret = dict()
    Engine = None
    ret['chrome-related'] = False
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
    if utils.config.has_section('chromium-linux'):
        Engine = builders.Headless()
        ret['chrome-related'] = True
    if utils.config.has_section('headless-patch'):
        Engine = builders.Headless_patch()
        ret['chrome-related'] = True
    if utils.config.has_section('chromium-win64'):
        Engine = builders.ChromiumWin64()
        ret['chrome-related'] = True

    ret['cpu'] = utils.config.get('main', 'cpu')
    ret['RepoPath'] = utils.RepoPath
    ret['modes'] = utils.config.get('main', 'modes')
    ret['hostname'] = utils.config.get(utils.config.get('main', 'slaves'), 'hostname')
    ret['source'] = Engine.source
    ret['engine'] = Engine
    return ret


if __name__ == '__main__':
    config1 = get_config_to_dict(options.config_name)
    build(options.config_name)
    dostuff(options.config_name, config1['engine'])

    if options.config2_name:
        config2 = get_config_to_dict(options.config2_name)
        if not config2['chrome-related']:
            build(options.config2_name)
        else:
            # if build the same chrome, skip build step.
            if config2['cpu'] != config1['cpu'] or \
                    config2['RepoPath'] != config1['RepoPath'] or \
                    config2['engine'].__class__ != config1['engine'].__class__ or \
                    config2['source'] != config1['source']:
                build(options.config2_name)
        dostuff(options.config2_name, config2['engine'])

    if options.config3_name:
        config3 = get_config_to_dict(options.config3_name)
        if not config3['chrome-related']:
            build(options.config3_name)
        else:
            # if build the same chrome, skip build step.
            if config3['cpu'] != config1['cpu'] or \
                    config3['RepoPath'] != config1['RepoPath'] or \
                    config3['engine'].__class__ != config1['engine'].__class__ or \
                    config3['source'] != config1['source']:
                if options.config2_name:
                    if config3['cpu'] != config2['cpu'] or \
                            config3['RepoPath'] != config2['RepoPath'] or \
                            config3['engine'].__class__ != config2['engine'].__class__ or \
                            config3['source'] != config2['source']:
                        build(options.config3_name)
                else:
                    build(options.config3_name)
        dostuff(options.config3_name, config3['engine'])
