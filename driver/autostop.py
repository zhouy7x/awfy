#!/usr/bin/python

import time, os

while True:
    file = "/logs/v8/schedule-run-v8-log--20190506095103.txt"
    with open(file) as f:
        data = f.read()

    if "5782a628581fd917242e8f9c5aa5dda7fda0ed89" in data:
        print os.system("python all_kill.py v8")
        time.sleep(3)
        break
    # print os.system("python all_run.py x64")
    print "sleep 10min..."
    time.sleep(10*60)

