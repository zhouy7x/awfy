#!/bin/bash -xv

logdir=log-`date +%Y%m%d%H%M%S`
mkdir /home/user/work/logs/$logdir

python query_server.py > /home/user/work/logs/$logdir/query_server_log.txt 2>&1 &

python build_server_v8.py > /home/user/work/logs/$logdir/build_server_v8_log.txt 2>&1 &
rm /tmp/awfy-daemon-v8
bash schedule-run-v8.sh > /home/user/work/logs/$logdir/schedule-run-v8-log.txt 2>&1 &

python build_server_chrome.py > /home/user/work/logs/$logdir/build_server_chrome_log.txt 2>&1 &
rm /tmp/awfy-daemon-chrome
bash schedule-run-chrome.sh > /home/user/work/logs/$logdir/schedule-run-chrome-log.txt 2>&1 &

python build_server_chrome_arm.py > /home/user/work/logs/$logdir/build_server_chrome_arm_log.txt 2>&1 &
rm /tmp/awfy-daemon-chrome-arm
bash schedule-run-chrome-arm.sh > /home/user/work/logs/$logdir/schedule-run-chrome-arm-log.txt 2>&1 &
