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

if [ -e /tmp/awfy-daemon ]
then
  echo "awfy: Already running"
  exit 0
fi

touch /tmp/awfy-daemon

count=0
date="Empty"

while :
do
  if [ -e /tmp/awfy ]
  then
    echo "awfy: /tmp/awfy lock in place"
    sleep 30m
  else
    hasUpdate="false"

    # First, check jerry update
    pushd /home/user/work/repos/jerryscript
        git fetch
        list=`git rev-list origin/master ^master | tac`
        if [ -z "$list" ]; then
          echo "jerry: no update"
        else
          hasUpdate="true"
          # Get every commit of jerryscript
          for i in $list
          do
            echo $i
            git reset --hard $i
            pushd /home/user/work/awfy/driver
            # Test jerry
            python dostuff.py -f -n --config=jerry-x86.config
            popd
          done
        fi
    popd

    # Second, check iotjs update
    pushd /home/user/work/repos/iotjs
        git fetch
        list=`git rev-list origin/master ^master | tac`
        if [ -z "$list" ]; then
          echo "iotjs: no update"
        else
          hasUpdate="true"
          # Get every commit of iotjs
          for i in $list
          do
            echo $i
            git reset --hard $i
            pushd /home/user/work/awfy/driver
            # Test iotjs
            python dostuff.py -f -n --config=iotjs-x86.config
            popd
          done
        fi
    popd

    today=`date +%Y-%m-%d`
    if [ "$today" != "$date" ]; then
        pushd /home/user/work/awfy/driver
        # Test jerry
        python passrate.py -f -n --config=jerry-x86.config
        popd
        date="$today"
    fi

    if [ "$hasUpdate" = "false" ]; then
      echo "awfy: no source update, sleep 15m"
      sleep 15m
    fi

  fi
done
rm /tmp/awfy-daemon

