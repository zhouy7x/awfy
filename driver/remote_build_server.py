# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
from sys import argv

try:
    build_driver = argv[1]
    build_host = argv[2]
    port = argv[3] if argv[3:] else 8799
except Exception as e:
    print "Error: You must give 3 params, BuildDriverPath, BuildHost and BuildPort!!!"
    raise Exception(e)

cmd = 'ssh ' + build_host + ' "powershell /c cd '+build_driver+' ; python build_server.py '+port+'"'
print cmd
os.system(cmd)
