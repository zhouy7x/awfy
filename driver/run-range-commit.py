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

count=0
if [ -e /tmp/awfy ]
then
	echo "/tmp/awfy lock in place"
else
        pushd /home/user/work/awfy/repos/v8
          list=`git rev-list 230d0845b7012bb404d013d0fce9d07fb83f62e2 ^aa84551622799c6c44b8ee60ea6c40405465177a | tac`
          if [ -z "$list" ]; then
            echo "no source updated, sleep 2m"
            sleep 120
          else
            for i in $list
            do
              echo $i
              git reset --hard $i
	      pushd /home/user/work/awfy/driver
	      python dostuff.py -f -n --config=awfy-x64.config
              python dostuff.py -f -n --config=awfy-x86.config

              count=`expr $count + 1`
              count=`expr $count % 5`
              if [ "$count" = "1" ]
              then
                python dostuff.py -f -n --config=awfy-arm.config
              fi

              popd
              pushd /home/user/work/awfy/server
              bash ./run-update.sh
              popd
            done
          fi
        popd
fi
rm /tmp/awfy-daemon

