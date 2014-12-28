#!/bin/bash

if [ -e /tmp/awfy-lock ]
then
  echo "Already running"
  exit 0
fi

touch /tmp/awfy-lock
/usr/bin/python /home/user/work/awfy/server/update.py
rm /tmp/awfy-lock

