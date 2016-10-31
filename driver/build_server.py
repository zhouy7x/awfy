# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import socket
import json, time
import utils
import builders
import resource

LISTEN_ADDRESS = "0.0.0.0"
LISTEN_PORT = 8787
ERROR_LOG_FILE = "build_server_error.log"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((LISTEN_ADDRESS, LISTEN_PORT))
s.listen(5)


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
	utils.InitConfig(config)
	# Set of engines that get build.
	KnownEngines = []

	if utils.config.has_section('v8'):
	    KnownEngines.append(builders.V8())
	if utils.config.has_section('contentshell'):
	    KnownEngines.append(builders.ContentShell())
	if utils.config.has_section('jerryscript'):
	    KnownEngines.append(builders.JerryScript())
	if utils.config.has_section('iotjs'):
	    KnownEngines.append(builders.IoTjs())
	Engines, NumUpdated = builders.build(KnownEngines, False, False)

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
s.close()


