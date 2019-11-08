#!/bin/bash -xv

# Protocol for stopping AWFY:
#
# (1) If you want to stop it immediately:
#     screen -r
#     ctrl+c
#     rm /tmp/awfy-daemon-chrome
#     rm /tmp/awfy
#     ctrl a+d
#     Remember to start it again later!
#
# (2) If you want to it to stop when possible:
#     touch /tmp/awfy
#     screen -r
#     (wait for it to confirm that it's no longer running)
#     ctrl a+d
lockfile=/tmp/awfy-daemon-1800x
if [ -e "$lockfile" ]
then
  echo "awfy: Already running"
  exit 0
fi

touch $lockfile

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
        pushd /home/user/work/repos/v8/1800x/v8
        git fetch
        list=`git rev-list origin/master ^master | tac | python /home/user/work/awfy/driver/v8-filter.py`
        if [ -z "$list" ]; then
            echo "v8: no update"
        else

            hasUpdate="true"
            # Get every commit of v8
            for id in $list
            do
                git reset --hard -q $id && gclient sync -f -j10
                git log -1 --pretty=short

                pushd /home/user/work/awfy/driver

                STARTT=$(date +%s)

                if [ ! -e tmp/1800x-v8-count ];
                then
                    touch tmp/1800x-v8-count
                fi
                tmp=`cat tmp/1800x-v8-count`;
                if [ -z "$tmp" ];
                then
                    tmp=0;
                fi
                echo $tmp;

                if [ $tmp == 70 ];
                then
                    string='-long-time';
                    tmp=0
                else
                    string='';
                    tmp=$[tmp+1];
                fi

                python dostuff-1800x.py --config=client/v8/amd-1800x-x64$string.config --config2=client/v8/amd-1800x-x86.config --config3=client/v8/amd-1800x-x64-patch.config $id &

                echo $tmp > tmp/v8-count;

                wait

                SECS=$(($(date +%s) - $STARTT))
                printf "\n++++++++++++++++ %dh:%dm:%ds ++++++++++++++++\n\n\n" $(($SECS/3600)) $(($SECS%3600/60)) $(($SECS%60))

                #sleep 10h

                popd

                pushd /home/user/work/awfy/server
                ./run-update.sh
                popd


                if [ -e /tmp/awfy-stop ]
                then
                    rm /tmp/awfy-daemon-chrome /tmp/awfy-stop
                    echo "awfy: Already stoped"
                    exit 0
                fi
            done
        fi
        popd

        # Second, check chromium update
        pushd /home/user/work/repos/chrome/1800x/chromium/src
        git fetch
        list=`git rev-list origin/master ^master | tac`
        if [ -z "$list" ]; then
            echo "chromium: no update"
        else
            for i in $list
            do
                # Only check v8 changed chromium
                v8find=`git show $i | grep -P "^\+\s+.v8_revision."`
                if [[ -n $v8find ]]; then
                    hasUpdate="true"
                    echo $i
                    git reset --hard $i
                    pushd /home/user/work/awfy/driver

                    STARTT=$(date +%s)

                    python dostuff-1800x.py  --config=client/chrome/amd-1800x.config
                    popd

                    wait

                    SECS=$(($(date +%s) - $STARTT))
                    printf "\n++++++++++++++++ %dh:%dm:%ds ++++++++++++++++\n\n\n" $(($SECS/3600)) $(($SECS%3600/60)) $(($SECS%60))

                    pushd /home/user/work/awfy/server
                    bash ./run-update.sh
                    popd
                fi
            done
        fi
        popd

        if [ "$hasUpdate" = "false" ]; then
            echo "awfy: no source update, sleep 15m"
            sleep 1m
        fi

    fi
done
rm $lockfile

