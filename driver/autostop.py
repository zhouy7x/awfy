#!/usr/bin/python

import time, os

while True:
    file = "/logs/chrome/electro/schedule-run-chrome-log--20190315101217.txt"
    with open(file) as f:
        data = f.read()

    if "732fc59039585cf57e181992c08c675b8d81f274" in data:
        print os.system("python all_kill.py x64")
        time.sleep(3)
        break
    # print os.system("python all_run.py x64")
    print "sleep 10min..."
    time.sleep(10*60)

