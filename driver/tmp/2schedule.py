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
while :
do
  if [ -e /tmp/awfy ]
  then
    echo "awfy: /tmp/awfy lock in place"
    sleep 30m
  else
    hasUpdate="false"

    # First, check v8 update
    pushd /home/user/work/repos/v8
    git fetch
    list=`git rev-list origin/master ^master | tac`
    if [ -z "$list" ]; then
      echo "v8: no update"
    else
      hasUpdate="true"
      # Get every commit of v8
      for i in $list
      do
        echo $i
        git reset --hard $i
        pushd /home/user/work/awfy/driver
        # Test x64 and x86 every time
        python dostuff.py -f -n --config=awfy-x64.config
        python dostuff.py -f -n --config=awfy-x86.config
  
        count=`expr $count + 1`
        count=`expr $count % 5`
        if [ "$count" = "1" ]
        then
          # Test arm every 5 times
          python dostuff.py -f -n --config=awfy-arm.config
        fi
  
        popd
        pushd /home/user/work/awfy/server
        bash ./run-update.sh
        popd
      done
    fi
    popd

    # Second, check chromium update
    pushd /home/user/work/repos/chromium/src
    git fetch
    list=`git rev-list origin/master ^master | tac`
    if [ -z "$list" ]; then
      echo "chromium: no update"
    else
      hasUpdate="true"
      for i in $list
      do
        # Only check v8 changed chromium
        v8find=`git show $i | grep -P "^\+\s+.v8_revision."`
        if [[ -n $v8find ]]; then
          echo $i
          pushd /home/user/work/awfy/driver
          python dostuff.py -f -n --config=awfy-contentshell.config
          popd

          pushd /home/user/work/awfy/server
          bash ./run-update.sh
          popd
        fi
      done
    fi
    popd

    # Third, check iotjs update
    pushd /home/user/work/repos/iotjs
    popd

    if [ "$hasUpdate" = "false" ]; then
      echo "awfy: no source update, sleep 30m"
      sleep 30m
    fi

  fi
done
rm /tmp/awfy-daemon

