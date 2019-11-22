#!/bin/bash

if [ -e /tmp/awfy-lock ]
then
  echo "Already running"
  exit 0
fi

touch /tmp/awfy-lock
rm -rf /home/user/work/awfy/website/data/
mkdir -p /home/user/work/awfy/website/data/

STARTT=$(date +%s)
/usr/bin/python /home/user/work/awfy/server/update.py
wait
SECS=$(($(date +%s) - $STARTT))
printf "\n++++++++++++++++ $0: %dh:%dm:%ds ++++++++++++++++\n\n\n" $(($SECS/3600)) $(($SECS%3600/60)) $(($SECS%60))

rm /tmp/awfy-lock
