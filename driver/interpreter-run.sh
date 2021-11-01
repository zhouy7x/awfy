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

python print_env.py

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
    list=`git rev-list origin/main...main | tac | python /home/user/work/awfy/driver/v8-filter.py`
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

        python dostuff.py -f -n --config=awfy-interpreter.config


        popd
      done
    fi
    popd

    if [ "$hasUpdate" = "false" ]; then
      echo "awfy: no source update, sleep 15m"
      sleep 15m
    fi

  fi
done
rm /tmp/awfy-daemon

