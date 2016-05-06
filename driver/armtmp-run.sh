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

if [ -e /tmp/awfy ]
then
  echo "awfy: /tmp/awfy lock in place"
  exit 0
else
  hasUpdate="false"

  # First, check v8 update
  pushd /home/user/work/awfy/repos/v8
  git fetch
  list=`git rev-list 45d75bca5c13f52850d9ac10ea58dae38fd0f1d7 ^master | tac`
  if [ -z "$list" ]; then
    echo "v8: no update"
  else
    hasUpdate="true"
    # Get every commit of v8
    for i in $list
    do
      count=`expr $count + 1`
      armtest=`expr $count % 5`
      if [ "$armtest" = "1" ]
      then
        echo $i
        git reset --hard $i
        
        pushd /home/user/work/awfy/driver
        # Test arm every 5 times
        python dostuff.py -f -n --config=awfy-arm.config
        popd
        pushd /home/user/work/awfy/server
        bash ./run-update.sh
        popd
      fi
    done
  fi
  popd

  # Second, check chromium update
  # no chromium for arm
fi

rm /tmp/awfy-daemon

