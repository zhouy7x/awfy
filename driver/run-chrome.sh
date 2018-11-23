#!/bin/bash

python build_server_chrome.py > /home/user/work/logs/log-20180802140244/build_server_chrome_log.txt 2>&1 &
rm /tmp/awfy-daemon-chrome
bash schedule-run-chrome.sh > /home/user/work/logs/log-20180802140244/schedule-run-chrome-log.txt 2>&1 &
