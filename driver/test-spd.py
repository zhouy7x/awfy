#!/bin/bash

count=1
while [ $count -le 10 ]; do
    echo $count
    ssh user@awfy-x64-spd.sh.intel.com -- "cd /home/user/work/awfy/driver ; python slaves.py /home/user/work/awfy/driver/state.p"
    count=$((count + 1))
    sleep 3
done
echo "finished"
