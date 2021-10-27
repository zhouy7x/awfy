#!/bin/bash

if [ -e /tmp/awfy-lock ]
then
  echo "Already running"
  exit 0
fi

touch /tmp/awfy-lock
# Using awfy2.py to write data to website/data2 folder.
# After complete, then remove old website/data folder and rename website/data2 to website/data.
rm -rf /home/user/work/awfy/website/data2/
mkdir -p /home/user/work/awfy/website/data2/
pushd /home/user/work/awfy/server
mv awfy.py awfy-bak.py ; mv awfy2.py awfy.py

STARTT=$(date +%s)
/usr/bin/python /home/user/work/awfy/server/update.py
wait

rm -rf /home/user/work/awfy/website/data
mv  /home/user/work/awfy/website/data2  /home/user/work/awfy/website/data
mv awfy.py awfy2.py ; mv awfy-bak.py awfy.py
popd
SECS=$(($(date +%s) - $STARTT))
printf "\n++++++++++++++++ $0: %dh:%dm:%ds ++++++++++++++++\n\n\n" $(($SECS/3600)) $(($SECS%3600/60)) $(($SECS%60))

rm /tmp/awfy-lock
