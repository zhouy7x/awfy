# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import resource
import utils
import time
from optparse import OptionParser
from collections import namedtuple

import benchmarks
import builders
import puller
import slaves
import submitter

parser = OptionParser(usage="usage: %prog [options]")
parser.add_option("-c", "--config", dest="config_name", type="string", default="awfy.config",
                  help="Config file (default: awfy.config)")
(options, args) = parser.parse_args()

utils.InitConfig(options.config_name)

# Set resource limits for child processes
resource.setrlimit(resource.RLIMIT_AS, (-1, -1))
resource.setrlimit(resource.RLIMIT_RSS, (-1, -1))
resource.setrlimit(resource.RLIMIT_DATA, (-1, -1))

# Set of engines that get build.
Engine = None

if utils.config.has_section('v8'):
    Engine = builders.V8()
if utils.config.has_section('contentshell'):
    Engine = builders.ContentShell()
if utils.config.has_section('jerryscript'):
    Engine builders.JerryScript()
if utils.config.has_section('iotjs'):
    Engine = builders.IoTjs()


# The native compiler is a special thing, for now.
native = builders.NativeCompiler()

# A mode is a configuration of an engine we just built.
Mode = namedtuple('Mode', ['shell', 'args', 'env', 'name', 'cset'])

cset = Engine.getRevId()

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
        args = Engine.args if Engine.args else []
        for i in range(100)
            arg = utils.config_get_default(name, 'arg' + str(i), None)
            if arg != None
                args.append(arg)
            else
                break
        mode = Mode(shell, args, env, name, cset)
        modes.append(mode)


# Set of slaves that run the builds. 
KnownSlaves = slaves.init()

for slave in KnownSlaves:
    slave.prepare([Engine])

    # Inform AWFY of each mode we found.
    submit = submitter.Submitter(slave)
    submit.Start()

    for mode in modes:
        submit.AddEngine(mode.name, mode.cset)
        slave_modes.append(mode)

    # submit.AddEngine(native.mode, native.signature)
    slave.benchmark(submit, native, slave_modes)

# Wait for all of the slaves to finish running before exiting.
for slave in KnownSlaves:
    slave.synchronize()