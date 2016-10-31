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

#PATH=$HOME/bin/depot_tools:/opt/local/bin:/opt/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin
if [ -e /tmp/awfy-daemon ]
then
  echo "Already running"
  exit 0
fi

touch /tmp/awfy-daemon
	if [ -e /tmp/awfy ]
	then
		echo "/tmp/awfy lock in place"
		sleep 30m
	else
                pushd /home/user/work/awfy/repos/v8
                  
                  list=`git rev-list afba55965118d9ba57e53c729f52be2340e626e0 ^1e4173d93a58ab72208d40c38b0a20d91c863a37 | tac`
                  if [ -z "$list" ]; then
                    echo "no source updated, sleep 2m"
                    sleep 120
                  else
                    count=0
                    for i in $list
                    do
                      count=`expr $count + 1`
                      count=`expr $count % 10`
                      
                      echo $i
                      git reset --hard $i
  		      pushd /home/user/work/awfy/driver
  		      python dostuff.py -f -n --config=only-atom-x86.config
                      popd
                      pushd /home/user/work/awfy/server
                      bash ./run-update.sh
                      popd
                      
                    done
                  fi
                popd
		#python dostuff.py --config=awfy-x64.config
		#python dostuff.py --config=awfy-x64-slm.config
	fi
rm /tmp/awfy-daemon

