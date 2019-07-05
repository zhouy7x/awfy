#!/usr/bin/python

import time, os
from sys import argv

file = argv[1]
commit = argv[2]

while True:
    #file = "/logs/v8/schedule-run-v8-log--20190628150834.txt"
    with open(file) as f:
        data = f.read()

    if "aad6df1dc4d82e88f3020a721b973e705dc82514" in data:
        print os.system("python all_kill.py v8")
        time.sleep(3)
        break
    # print os.system("python all_run.py x64")
    print "sleep 10min..."
    time.sleep(10*60)

