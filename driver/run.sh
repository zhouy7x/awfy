#!/bin/bash

# Protocol for stopping AWFY:
#
# (1) If you want to stop it immediately:
#     screen -r
#     ctrl+c
#     rm /tmp/awfy-daemon
#     rm /tmp/awfy
#     ctrl a+d
#     Remember to start it again later!
#
# (2) If you want to it to stop when possible:
#     touch /tmp/awfy
#     screen -r
#     (wait for it to confirm that it's no longer running)
#     ctrl a+d

PATH=$HOME/bin/depot_tools:/opt/local/bin:/opt/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin
if [ -e /tmp/awfy-daemon ]
then
  echo "Already running"
  exit 0
fi

touch /tmp/awfy-daemon
while :
do
	if [ -e /tmp/awfy ]
	then
		echo "/tmp/awfy lock in place"
		sleep 30m
	else
		cd /home/user/work/awfy/driver
		python dostuff.py --config=awfy-x64.config
                pushd ../server
                bash ./run-update.sh
                popd
		#python dostuff.py --config=awfy-x64-slm.config
	fi
done
rm /tmp/awfy-daemon

