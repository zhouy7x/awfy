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
  #exit 0
fi

python returntest.py
echo $?
exit 0
#touch /tmp/awfy-daemon

count=0
while :
do
  if [ -e /tmp/awfy ]
  then
    echo "awfy: /tmp/awfy lock in place"
    break
  else
    hasUpdate="false"

    # First, check v8 update
    pushd /home/user/work/awfy/repos/v8
    list=`git rev-list origin/master ^master | tac`
    if [ -z "$list" ]; then
      echo "v8: no update"
    else
      hasUpdate="true"
      # Get every commit of v8
      for i in $list
      do
        echo "v8:$i"
        pushd /home/user/work/awfy/driver
        # Test x64 and x86 every time
  
        popd
        pushd /home/user/work/awfy/server
        popd
      done
    fi
    popd

    # Second, check chromium update
    pushd /home/user/work/awfy/repos/chromium/src
    list=`git rev-list origin/master ^master | tac`
    if [ -z "$list" ]; then
      echo "chromium: no update"
    else
      for i in $list
      do
        # Only check v8 changed chromium
        v8find=`git show $i | grep -P "^\+\s+.v8_revision."`
        if [[ -n $v8find ]]; then
          echo "chromium:$i"
          hasUpdate="true"
          pushd /home/user/work/awfy/driver
          popd

          pushd /home/user/work/awfy/server
          popd
        fi
      done
    fi
    popd

    # Third, check iotjs update
    pushd /home/user/work/awfy/repos/iotjs
    popd

    if [ "$hasUpdate" = "false" ]; then
      echo "awfy: no source update, sleep 15m"
      sleep 15m
    fi

  fi
done
rm /tmp/awfy-daemon

