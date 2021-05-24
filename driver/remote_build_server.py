# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import time
from sys import argv
import utils

try:
    config_name = argv[1]
    utils.InitConfig(config_name)
except Exception as e:
    print "Error: You must give a right config file path!!!"
    # raise Exception(e)
else:
    build_driver = utils.config_get_default('main', 'build_driver')
    build_host = utils.config_get_default('main', 'build_host')
    port = utils.config_get_default('main', 'port', 8799)
    while True:
        cmd = 'ssh ' + build_host + ' "cd ' + build_driver + ' ; python build_server.py ' + str(port) + '"'
        print cmd
        os.system(cmd)
        time.sleep(5)
        cmd = 'ssh ' + build_host + ' "powershell /c cd ' + build_driver + ' ; python build_server.py ' + str(port)+'"'
        print cmd
        os.system(cmd)
        time.sleep(5)
