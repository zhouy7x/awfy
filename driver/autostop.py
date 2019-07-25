#!/usr/bin/python

import time, os
from sys import argv

try:
    file = argv[1]
    commit = argv[2]
except:
    raise Exception('Must input log file path and commit id!')

while True:
    #file = "/logs/v8/schedule-run-v8-log--20190628150834.txt"
    with open(file) as f:
        data = f.read()

    if commit in data:
        print os.system("python all_kill.py v8")
        time.sleep(3)
        break
    # print os.system("python all_run.py x64")
    print "sleep 10min..."
    time.sleep(10*60)

