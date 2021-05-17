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
  if [ ! -d "$1" ] ; then
    mkdir -p "$1"
  fi
  local list=`ls $1`
  local item="$2"
  if [[ $list =~ (^|[[:space:]])"$item"($|[[:space:]]) ]] ; then
    # yes, list include item, reset the freq.
    echo $v8_longtime_bench_freq > $v8countfile
  fi
}

function create_position(){
    if [ ! -d $v8_longtime_bench_commit_dir ]; then
        mkdir -p $v8_longtime_bench_commit_dir
    fi
    pushd $v8_longtime_bench_commit_dir
    touch $1
    popd
}

v8_longtime_bench_commit_dir=tmp/v8_1800x_longtime_bench_commit
base_v8_longtime_bench_commit_dir=tmp/v8_longtime_bench_commit
lockfile=/tmp/awfy-daemon-win64
v8countfile=tmp/win64-v8-count
v8_longtime_bench_freq=70
build_server=ssgs3@ssgs3-test.sh.intel.com
#[ -z $1 ] && fast_forward=1 || fast_forward=$1
fast_forward=1

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
        echo "start remote check win64 v8 update>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
#        sleep 2m
        ssh $build_server "powershell /c cd d:/src/v8/v8/ ; git fetch"
        echo 'stop remote check win64 v8 update<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
        list=`ssh $build_server "powershell /c cd d:/src/v8/v8/ ; git rev-list origin/master...master" | tac | python /home/user/work/awfy/driver/v8-filter-win64.py`

        if [ -z "$list" ]; then
            echo "v8: no update"
        else

            hasUpdate="true"
            ignoreCount=0
            # Get every commit of v8
            for id in $list
            do
                ignoreCount=`expr $ignoreCount + 1`
                echo $ignoreCount
                if [ "$ignoreCount" -ge "$fast_forward" ]; then
                    ignoreCount=0
                else
                    continue
                fi
                ssh $build_server "powershell /c cd d:/src/v8/v8/ ; git reset --hard -q $id ; gclient sync -D -f -j10"
                ssh $build_server "powershell /c cd d:/src/v8/v8/ ; git log -1 --pretty=short"

                pushd /home/user/work/awfy/driver

                STARTT=$(date +%s)

                echo $id
                #check that if it is necessary to change the longtime bench freq.
                list_include_item $base_v8_longtime_bench_commit_dir $id

                if [ ! -e $v8countfile ]; then
                    touch $v8countfile
                fi
                tmp=`cat $v8countfile`;
                if [ -z "$tmp" ]; then
                    tmp=0;
                fi
#                echo $tmp;

                if [ $tmp == $v8_longtime_bench_freq ]; then
                    create_position $id;
                    string='-long-time';
                    tmp=0
                else
                    string='';
                    tmp=$[tmp+1];
                fi
                string='';

#                python dostuff_win64.py --config=client/win64-v8/amd-1800x-x64$string.config --config2=client/win64-v8/amd-1800x-x86.config $id &
                #python dostuff_win64.py --config=client/win64-v8/amd-3900x-x64$string.config --config2=client/win64-v8/amd-3900x-x86.config $id &
                python dostuff_win64.py --config=client/win64-v8/amd-3900x-x64$string.config $id &
#                python dostuff_win64.py --config=client/win64-v8/intel-9700-x64$string.config --config2=client/win64-v8/intel-9700-x86.config $id &
                #python dostuff_win64.py --config=client/win64-v8/intel-9900k-x64$string.config --config2=client/win64-v8/intel-9900k-x86.config $id &
                python dostuff_win64.py --config=client/win64-v8/intel-9900k-x64$string.config $id &
#                python dostuff_win64.py --config=client/win64-v8/intel-8700k-x64$string.config --config2=client/win64-v8/intel-8700k-x86.config $id &
#                python dostuff_win64.py --config=client/win64-v8/amd-3800x-x64$string.config --config2=client/win64-v8/amd-3800x-x86.config $id &

                echo $tmp > $v8countfile;

                wait

                SECS=$(($(date +%s) - $STARTT))
                printf "\n++++++++++++++++ $0: %dh:%dm:%ds ++++++++++++++++\n\n\n" $(($SECS/3600)) $(($SECS%3600/60)) $(($SECS%60))

                #sleep 10h

                popd

                pushd /home/user/work/awfy/server
                printf "\n+++++ start run-update.sh +++++\n"
                ./run-update.sh > /dev/null &
                popd

                count=`expr $count + 1`
                echo $count
                if [ "$count" -ge 6 ]; then
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

        # Second, check chromium update
        count=0
        echo "start remote check win64 chromium update>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
#        sleep 2m
        ssh $build_server "powershell /c cd d:/src/chromium/src/ ; git fetch"
        echo 'stop remote check win64 chromium update<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
        list=`ssh $build_server "powershell /c cd d:/src/chromium/src/ ; git rev-list origin/master...master" | tac`
        if [ -z "$list" ]; then
            echo "chromium: no update"
        else
            for i in $list
            do
                # Only check v8 changed chromium
                v8find=`ssh $build_server "powershell /c cd d:/src/chromium/src/ ; git show $i "| grep -P "^\+\s+.v8_revision."`
                if [[ -n $v8find ]]; then
                    hasUpdate="true"
                    echo $i
                    ssh $build_server "powershell /c cd d:/src/chromium/src/ ; git reset --hard $i"

                    pushd /home/user/work/awfy/driver

                    STARTT=$(date +%s)

                    #python dostuff_win64.py --config=client/win64-chrome/amd-1800x.config --config2=client/win64-chrome/intel-8700k.config --config3=client/win64-chrome/amd-3800x.config $i
#                    python dostuff_win64.py --config=client/win64-chrome/amd-1800x.config --config2=client/win64-chrome/intel-9700.config $i
                    python dostuff_win64.py --config=client/win64-chrome/amd-3900x.config --config2=client/win64-chrome/intel-9900k.config $i

                    popd

                    wait

                    SECS=$(($(date +%s) - $STARTT))
                    printf "\n++++++++++++++++ $0: %dh:%dm:%ds ++++++++++++++++\n\n\n" $(($SECS/3600)) $(($SECS%3600/60)) $(($SECS%60))

                    pushd /home/user/work/awfy/server
                    printf "\n+++++ start run-update.sh +++++\n"
                    ./run-update.sh > /dev/null &
                    popd

                    count=`expr $count + 1`
                    if [ "$count" -ge 2 ]; then
                        break
                    fi
                fi
            done
        fi


        if [ "$hasUpdate" = "false" ]; then
            echo "awfy: no source update, sleep 15m"
            sleep 1m
        fi

    fi
done
rm $lockfile

