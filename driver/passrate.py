# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import resource
import utils
import time
import datetime
from optparse import OptionParser
from collections import namedtuple

import benchmarks
import builders
import puller
import slaves
import submitter

parser = OptionParser(usage="usage: %prog [options]")
parser.add_option("-f", "--force", dest="force", action="store_true", default=False,
                  help="Force runs even without source changes")
parser.add_option("-n", "--no-update", dest="noupdate", action="store_true", default=False,
                  help="Skip updating source repositories")
parser.add_option("-c", "--config", dest="config_name", type="string", default="awfy.config",
                  help="Config file (default: awfy.config)")
(options, args) = parser.parse_args()

utils.InitConfig(options.config_name)

# Set resource limits for child processes
resource.setrlimit(resource.RLIMIT_AS, (-1, -1))
resource.setrlimit(resource.RLIMIT_RSS, (-1, -1))
resource.setrlimit(resource.RLIMIT_DATA, (-1, -1))

# No Set of engines that get build.

# A mode is a configuration of an engine we just built.
Mode = namedtuple('Mode', ['shell', 'args', 'env', 'name', 'cset'])

# Only one mode run
shell = builders.JerryScript().shell()
args = []
env = os.environ.copy()
name = 'JerryScript-x86'
cset = "%s" % datetime.date.today()

mode = Mode(shell, args, os.environ.copy(), name, cset)

# Change test benchmark to passrate
benchmarks.Benchmarks = [benchmarks.JerryPassrate()]

# Set of slaves that run the builds. 
KnownSlaves = slaves.init()

for slave in KnownSlaves:
    #slave.prepare(Engines)

    # Inform AWFY of each mode we found.
    submit = submitter.Submitter(slave)
    submit.Start()
    submit.AddEngine(mode.name, mode.cset)

    # passrate do not need native
    slave.benchmark(submit, None, modes)

# Wait for all of the slaves to finish running before exiting.
for slave in KnownSlaves:
    slave.synchronize()
