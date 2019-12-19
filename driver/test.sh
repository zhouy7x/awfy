#!/bin/bash

function list_include_item(){
  local list=`ls $1`
  local item="$2"
  if [[ $list =~ (^|[[:space:]])"$item"($|[[:space:]]) ]] ; then
    # yes, list include item
    result=0
    echo $v8_longtime_bench_freq > $v8countfile
  else
    result=1
  fi
  echo $result
  return $result
}

function create_position(){
    if [ ! -e $v8_longtime_bench_commit_dir ]; then
        mkdir -p $v8_longtime_bench_commit_dir
    fi
    pushd $v8_longtime_bench_commit_dir
    touch $1
    popd
}

v8_longtime_bench_commit_dir=tmp/v8_longtime_bench_commit
base_v8_longtime_bench_commit_dir=tmp/v8_1800x_longtime_bench_commit
v8countfile=tmp/1800x-v8-count
v8_longtime_bench_freq=70

pushd /home/benchmark/v8/v8
#git fetch
list=`git rev-list origin/master ^master | tac | python /home/benchmark/awfy/driver/v8-filter.py`
if [ -z "$list" ]; then
    echo "v8: no update"
else

    hasUpdate="true"
    # Get every commit of v8
    for id in $list;
    do
        #git reset --hard -q $id && git clean -fd && gclient sync -f -j10
        #git log -1 --pretty=short

        pushd /home/benchmark/awfy/driver

        STARTT=$(date +%s)
        echo $id
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

        sleep 1
        echo $tmp > $v8countfile;
        wait
        popd
    done
fi