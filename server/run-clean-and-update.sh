#!/bin/bash  -xv

if [ -e /tmp/awfy-lock ]
then
  echo "Already running"
  exit 0
fi

touch /tmp/awfy-lock
rm -rf /home/user/work/awfy/website/data/* 
#cp /home/user/work/awfy/website/master.js /home/user/work/awfy/website/data
/usr/bin/python /home/user/work/awfy/server/update.py
rm /tmp/awfy-lock
