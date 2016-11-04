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

trap "kill 0" EXIT

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
    pushd /home/user/work/awfy/repos/v8
    git fetch
    list=`git rev-list origin/master ^master | tac | python /home/user/work/awfy/driver/v8-filter.py`
    if [ -z "$list" ]; then
      echo "v8: no update"
    else
      hasUpdate="true"
      # Get every commit of v8
      for id in $list
      do
        git reset --hard -q $id && gclient sync -j8
        git log -1
        rm -f out/arm.release/d8 out/ia32.release/d8 out/x64.release/d8

        pushd /home/user/work/awfy/driver

        STARTT=$(date +%s)

        python dostuff.py --config=client/hsw-nuc-x64.config --config2=client/hsw-nuc-x86.config $id &

        sleep 5s

        python dostuff.py --config=client/atom-nuc-x86.config --config2=client/atom-nuc-x64.config $id &

        python dostuff.py --config=client/atom-nuc-2-x64.config --config2=client/atom-nuc-2-x86.config $id &

        python dostuff.py --config=client/chrubuntu-arm.config $id &

        python dostuff.py --config=client/chromeos-arm.config $id &

        python dostuff.py --config=client/fc-interp-x64.config $id &

        wait

        SECS=$(($(date +%s) - $STARTT))
        printf "\n++++++++++++++++ %dh:%dm:%ds ++++++++++++++++\n\n\n" $(($SECS/3600)) $(($SECS%3600/60)) $(($SECS%60))

        #sleep 10h

        popd
        pushd /home/user/work/awfy/server
        ssh user@user-awfy.sh.intel.com "cd /home/user/work/awfy/server ; bash run-update.sh"
        popd
      done
    fi
    popd

    # Second, check chromium update
    # pushd /home/user/work/awfy/repos/chromium/src
    # git fetch
    # list=`git rev-list origin/master ^master | tac`
    # if [ -z "$list" ]; then
    #   echo "chromium: no update"
    # else
    #   for i in $list
    #   do
    #     # Only check v8 changed chromium
    #     v8find=`git show $i | grep -P "^\+\s+.v8_revision."`
    #     if [[ -n $v8find ]]; then
    #       hasUpdate="true"
    #       echo $i
    #       git reset --hard $i
    #       pushd /home/user/work/awfy/driver
    #       python dostuff.py -f -n --config=awfy-contentshell.config
    #       popd

    #       pushd /home/user/work/awfy/server
    #       bash ./run-update.sh
    #       popd
    #     fi
    #   done
    # fi
    # popd

    if [ "$hasUpdate" = "false" ]; then
      echo "awfy: no source update, sleep 15m"
      sleep 15m
    fi

  fi
done
rm /tmp/awfy-daemon

