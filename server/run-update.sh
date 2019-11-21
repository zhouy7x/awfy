#!/bin/bash

if [ -e /tmp/awfy-lock ]
then
  echo "Already running"
  exit 0
fi
touch /tmp/awfy-lock
STARTT=$(date +%s)
/usr/bin/python /home/user/work/awfy/server/update.py
wait
SECS=$(($(date +%s) - $STARTT))
printf "\n++++++++++++++++ %dh:%dm:%ds ++++++++++++++++\n\n\n" $(($SECS/3600)) $(($SECS%3600/60)) $(($SECS%60))
rm /tmp/awfy-lock
