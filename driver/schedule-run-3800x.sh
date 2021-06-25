#!/bin/bash -xv

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

function list_include_item(){
  local list=`ls $1`
  local item="$2"
  if [[ $list =~ (^|[[:space:]])"$item"($|[[:space:]]) ]] ; then
    # yes, list include item, reset the freq.
    echo $v8_longtime_bench_freq > $v8countfile
  fi
}

function create_position(){
    if [ ! -e $v8_longtime_bench_commit_dir ]; then
        mkdir -p $v8_longtime_bench_commit_dir
    fi
    pushd $v8_longtime_bench_commit_dir
    touch $1
    popd
}

v8_longtime_bench_commit_dir=tmp/v8_3800x_longtime_bench_commit
base_v8_longtime_bench_commit_dir=tmp/v8_longtime_bench_commit
lockfile=/tmp/awfy-daemon-3800x
v8countfile=tmp/3800x-v8-count
v8_longtime_bench_freq=70

if [ -e "$lockfile" ]
then
  echo "awfy: Already running"
  exit 0
fi

touch $lockfile

trap "kill 0" EXIT

python print_env.py


while :
do
    if [ -e /tmp/awfy ]
    then
        echo "awfy: /tmp/awfy lock in place"
        sleep 30m
    else
        hasUpdate="false"

        # First, check v8 update
        count=0
        pushd /home/user/work/repos/v8/3800x/v8
        git fetch
        list=`git rev-list origin/master ^master | tac | python /home/user/work/awfy/driver/v8-filter.py`
        if [ -z "$list" ]; then
            echo "v8: no update"
        else

            hasUpdate="true"
            # Get every commit of v8
            for id in $list
            do
                git reset --hard -q $id && gclient sync -D -f -j10
                git log -1 --pretty=short

                pushd /home/user/work/awfy/driver

                STARTT=$(date +%s)

                echo $id
                #3800x runs slower than v8, so let 3800x change the longtime bench freq.
                list_include_item $base_v8_longtime_bench_commit_dir $id

                if [ ! -e $v8countfile ]; then
                    touch $v8countfile
                fi
                tmp=`cat $v8countfile`;
                if [ -z "$tmp" ]; then
                    tmp=0;
                fi
                echo $tmp;

                if [ $tmp == $v8_longtime_bench_freq ]; then
                    create_position $id;
                    string='-long-time';
                    tmp=0
                else
                    string='';
                    tmp=$[tmp+1];
                fi
                string='';

                # python dostuff_3800x.py --config=client/v8/amd-3800x-x64$string.config --config2=client/v8/amd-3800x-x86.config --config3=client/v8/amd-3800x-x64-patch.config $id &
                python dostuff_3800x.py --config=client/tmp/amd-3800x-x64$string.config --config2=client/tmp/amd-3800x-x86.config $id &

                echo $tmp > $v8countfile;

                wait

                SECS=$(($(date +%s) - $STARTT))
                printf "\n++++++++++++++++ $0: %dh:%dm:%ds ++++++++++++++++\n\n\n" $(($SECS/3600)) $(($SECS%3600/60)) $(($SECS%60))

                #sleep 10h

                popd

                pushd /home/user/work/awfy/server
                ./run-update.sh > /dev/null &
                popd

                count=`expr $count + 1`
                if [ "$count" -ge 20 ]; then
                    break
                fi

                if [ -e /tmp/awfy-stop ]
                then
                    rm $lockfile /tmp/awfy-stop
                    echo "awfy: Already stoped"
                    exit 0
                fi
            done
        fi
        popd

        # Second, check chromium update
        count=0
        pushd /home/user/work/repos/chrome/3800x/chromium/src
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

                    python dostuff_3800x.py  --config=client/tmp/amd-3800x.config
                    popd

                    wait

                    SECS=$(($(date +%s) - $STARTT))
                    printf "\n++++++++++++++++ $0: %dh:%dm:%ds ++++++++++++++++\n\n\n" $(($SECS/3600)) $(($SECS%3600/60)) $(($SECS%60))

                    pushd /home/user/work/awfy/server
                    ./run-update.sh > /dev/null &
                    popd

                    count=`expr $count + 1`
                    if [ "$count" -ge 10 ]; then
                        break
                    fi
                fi
            done
        fi
        popd

        if [ "$hasUpdate" = "false" ]; then
            echo "awfy: no source update, sleep 15m"
            sleep 15m
        fi

    fi
done
rm $lockfile

