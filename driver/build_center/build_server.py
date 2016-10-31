# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import socket
import redis
import threading
import json, time
import utils
import resource

from build_center_config import DB_HOST, DB_PORT, BUILD_JOB_DB_INDEX, \
	LISTEN_PORT, LISTEN_ADDRESS, ERROR_LOG_FILE

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((LISTEN_ADDRESS, LISTEN_PORT))
s.listen(5)


BUILD_SERVER_CONFIG = "build_server.config"


# Set resource limits for child processes
resource.setrlimit(resource.RLIMIT_AS, (-1, -1))
resource.setrlimit(resource.RLIMIT_RSS, (-1, -1))
resource.setrlimit(resource.RLIMIT_DATA, (-1, -1))

"""
    config format
    	{
    		"cpu": "x64",
    		"commit_id": "cedddd.....",
    		"hostname": "user@hsw-nuc.sh.intel.com",
    		"flag": "hardfp",
    		"force: 1 # 0,
    		"noupdate": 1 # 0
    		"repos": "/usr/local/awfy/repos",
    		"benchmark": "/usr/local/awfy/benchmarks",
    		"driver": "/usr/local/awfy/driver",
    		"python": "python",
    		"includes: "octane",
    		"machine":6,
    		"name": "hw",
    		"v8": {
				"source": "v8"
    		},
    		"iotjs": {
				"source": "iotjs"
    		},
    		"jerryscript": {
    			"source": "jerryscript"
    		}
    	}
"""

def build(config):
	file = open(BUILD_SERVER_CONFIG, "r")
	server_config = json.loads(file.read())
	utils.InitConfig(server_config, config)
	helper_config = {"1":True,"0":False}
	# Set of engines that get build.
	KnownEngines = []

	if 'v8' in config:
	    KnownEngines.append(builders.V8())
	if 'contentshell' in config:
	    KnownEngines.append(builders.ContentShell())
	if 'jerryscript' in config:
	    KnownEngines.append(builders.JerryScript())
	if 'iotjs' in config:
	    KnownEngines.append(builders.IoTjs())

	Engines, NumUpdated = builders.build(KnownEngines, not helper_config[config.noupdate], helper_config[config.force])

	# No updates. Report to server and wait 60 seconds, before moving on
	if NumUpdated == 0 and not options.force:
	    pass

	# The native compiler is a special thing, for now.
	native = builders.NativeCompiler()

	# A mode is a configuration of an engine we just built.
	Mode = namedtuple('Mode', ['shell', 'args', 'env', 'name', 'cset'])

	# Make a list of all modes.
	modes = []
	for engine in Engines:
	    shell = os.path.join(utils.RepoPath, engine.source, engine.shell())
	    env = None
	    with utils.chdir(os.path.join(utils.RepoPath, engine.source)):
	        env = engine.env()
	    for m in engine.modes:
	        engineArgs = engine.args if engine.args else []
	        modeArgs = m['args'] if m['args'] else []
	        args = engineArgs + modeArgs
	        mode = Mode(shell, args, env, m['mode'], engine.cset)
	        modes.append(mode)

	# Set of slaves that run the builds. 
	KnownSlaves = slaves.init()

	for slave in KnownSlaves:
	    slave.prepare(Engines)

	    # Inform AWFY of each mode we found.
	    submit = submitter.Submitter(slave)
	    submit.Start()

	    # modes only run on specific slave
	    slave_modes = []
	    for mode in modes:
	        # Do not run turbo on slm .I add this statement here for convenience.
	        # Though it's ugly. 
	        if slave.name == 'slm' and '--turbo' in mode.args:
	            continue
	        submit.AddEngine(mode.name, mode.cset)
	        slave_modes.append(mode)
	    submit.AddEngine(native.mode, native.signature)

	    slave.benchmark(submit, native, slave_modes)

	# Wait for all of the slaves to finish running before exiting.
	for slave in KnownSlaves:
	    slave.synchronize()



def log_to_file(err_content):
	file = open(ERROR_LOG_FILE, "a+")
	error_log = "error in build_server - %s : %s \n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), err_content)
	file.write(error_log)
	file.close()
while True:
	try:
		sock, addr = s.accept()
		print "connect", addr
		sock.send("connect ok")
		data = sock.recv(10240)
		if not data:
			log_to_file("client close in error with ip " + addr)
			continue
		print "recv", data
		# time.sleep(15)
		build(data)
		sock.send("over")
		sock.close()
		print "over"
		# t = threading.Thread(target = tcplink, args=(sock, addr))
		# t.start()
	except Exception,e:
		log_to_file(str(e))
		sock.send("error")
		sock.close()



